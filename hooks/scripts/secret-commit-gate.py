#!/usr/bin/env python3
"""Hook PreToolUse (Bash): gate de segredo no commit. Bloqueio, FAIL-CLOSED.

Regra da fatia 001 (plano, seção "Contratos"): intercepta `git commit` e roda
`gitleaks git --pre-commit --staged` com a config do repo (o plano nomeou
`protect --staged`, que o gitleaks deprecou; a rodada de correção do Veredito
migrou após verificar com o binário 8.30.1 que o comando novo se comporta
igual nos casos da suíte: achado ⇒ exit 1 + report JSON com os mesmos campos,
staged limpo ⇒ exit 0). Achado bloqueia o commit.
Qualquer falha do próprio gate (gitleaks ausente do PATH, erro de execução,
timeout, config ausente, entrada ilegível) também bloqueia: fail-closed, sem
varredura nenhum commit passa. Nenhum caminho de erro passa em silêncio.

Mecanismo de bloqueio (documentado): saída JSON de PreToolUse com
`hookSpecificOutput.permissionDecision: "deny"` + `permissionDecisionReason`,
e exit 0. É o mecanismo que o Claude Code documenta para negar a ferramenta
em PreToolUse (o exit 2 com stderr é o equivalente legado). A razão vai para
o modelo e para o usuário; a ferramenta não executa.

Detecção de `git commit` (documentada, simples de propósito):
  1. Remove segmentos entre aspas simples e duplas do comando (evita o falso
     positivo óbvio de `echo "git commit ..."`). A remoção é ingênua: não
     entende aspas aninhadas nem escapes.
  2. Procura `git`, seguido de zero ou mais opções com hífen (`-C <dir>`,
     `-c <cfg>`, `--flag[=v]`), seguido da palavra `commit`.
Limites declarados (lacuna já nomeada no plano e documentada em T08): alias
de shell, `sh -c 'git commit'` e outras indireções ficam FORA do match
(falso negativo); um comando que só menciona `git commit` fora de aspas
(ex.: `grep git commit`) entra no match (falso positivo), o que no máximo
roda uma varredura a mais — o gate erra para o lado de varrer. A linha
autoritativa contra bypass é a varredura no CI.

Resolução de caminho: a raiz do repo vem de `git rev-parse --show-toplevel`
executado no `cwd` do tool-input (o cwd da sessão onde o Bash vai rodar),
nunca no cwd do processo do hook — path relativo ao cwd do processo já
quebrou hook nesta fatia (ver README, registro do settings.json). A config
é `<raiz>/.gitleaks.toml` (onde a adoção a instala); ausente ⇒ fail-closed.

Segurança da saída (modelagem de ameaça do plano):
  - `--redact=80` sempre: o report só carrega o valor mascarado (ex.:
    `AKIA...`), nunca o segredo inteiro; 80%+ do valor some no gitleaks,
    antes de chegar a este wrapper.
  - A saída bruta do gitleaks (stdout/stderr) é capturada e NUNCA repassada.
    A mensagem usa só campos estruturados do report JSON: File, StartLine,
    RuleID, Secret (já mascarado).
  - O report vai para arquivo temporário criado com mkstemp (modo 0600) e
    apagado no finally: sem report residual em disco.

Desempenho (orçamento do plano): caso não-commit é só parse de JSON + regex,
~instantâneo; caso commit p95 < 1s (o `git --pre-commit --staged` varre só o
diff staged). Timeout de 30s na varredura ⇒ fail-closed.

Texto das mensagens: catálogo `hooks/mensagens.md`, seção 3.
Somente stdlib do Python 3.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

# Percentual de redação do gitleaks: 80% do valor vira "...", sobra no
# máximo o prefixo (ex.: AKIA...). Nunca rodar sem --redact.
REDACT = "80"

TIMEOUT_GIT = 10  # segundos, git rev-parse
TIMEOUT_GITLEAKS = 30  # segundos, varredura
MAX_ACHADOS_NA_MENSAGEM = 10

# git [opções com hífen]* commit — avaliado sobre o comando SEM os trechos
# entre aspas (ver docstring, detecção).
RE_GIT_COMMIT = re.compile(
    r"\bgit(?:\s+(?:-C\s+\S+|-c\s+\S+|--?[\w-]+(?:=\S+)?))*\s+commit\b"
)
RE_ASPAS = re.compile(r"'[^']*'|\"[^\"]*\"")

MSG_ACHADO_CABECALHO = "Bloqueado: segredo detectado no commit. "
MSG_ACHADO_LINHA = "`{arquivo}:{linha}`, padrão {tipo}, valor `{valor_mascarado}`."
MSG_ACHADO_RODAPE = (
    '\n\nRegra: constituição, seção "O que nunca fazer" '
    '("Nunca colocar segredo no repositório").\n\n'
    "Caminho: o segredo sai do código e vai pra variável de ambiente; a chave "
    "se documenta no `.env.example`, nunca o valor. Depois, `git add` e repita "
    "o commit. Falso positivo entra no `.gitleaks.toml` via PR (allowlist "
    "versionada, path exato). A varredura no CI é a linha autoritativa: "
    "contornar este gate não passa do PR."
)

MSG_FAIL_CLOSED = (
    "Bloqueado: o gate de segredo não conseguiu rodar ({motivo}). "
    "O gate é fail-closed: sem varredura, nenhum commit passa.\n\n"
    'Regra: constituição, seção "O que nunca fazer" '
    '("Nunca colocar segredo no repositório").\n\n'
    "Caminho: instale o gitleaks e repita o commit:\n\n"
    "`brew install gitleaks`\n\n"
    "Linux (binário oficial, ajuste versão e arquitetura):\n\n"
    "`curl -sSL https://github.com/gitleaks/gitleaks/releases/download/"
    "v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz | tar -xz gitleaks && "
    "sudo mv gitleaks /usr/local/bin/`\n\n"
    "Versão mínima: README do plugin, "
    'seção "Pré-requisito: gitleaks".'
)


def nega(mensagem):
    """Bloqueia a ferramenta: JSON de PreToolUse com permissionDecision deny."""
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": mensagem,
                }
            },
            ensure_ascii=False,
        )
    )
    sys.exit(0)


def e_git_commit(comando):
    """True se o comando contém uma invocação de git commit (ver docstring)."""
    return bool(RE_GIT_COMMIT.search(RE_ASPAS.sub(" ", comando)))


def raiz_do_repo(cwd):
    """Raiz do repo via git rev-parse --show-toplevel a partir do cwd do tool-input."""
    resultado = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_GIT,
    )
    if resultado.returncode != 0:
        return None
    raiz = resultado.stdout.strip()
    return raiz or None


def mensagem_de_achados(achados):
    """Monta a mensagem do catálogo só com campos estruturados do report."""
    linhas = []
    for achado in achados[:MAX_ACHADOS_NA_MENSAGEM]:
        linhas.append(
            MSG_ACHADO_LINHA.format(
                arquivo=achado.get("File") or "?",
                linha=achado.get("StartLine") or "?",
                tipo=achado.get("RuleID") or "?",
                valor_mascarado=achado.get("Secret") or "REDACTED",
            )
        )
    excedente = len(achados) - MAX_ACHADOS_NA_MENSAGEM
    if excedente > 0:
        linhas.append(f"(+{excedente} achado(s) além destes.)")
    return MSG_ACHADO_CABECALHO + "\n".join(linhas) + MSG_ACHADO_RODAPE


def roda_gate(cwd):
    """Roda o gitleaks no diff staged. Só retorna no caso limpo; senão, nega."""
    try:
        raiz = raiz_do_repo(cwd)
    except (subprocess.TimeoutExpired, OSError):
        raiz = None
    if not raiz:
        nega(MSG_FAIL_CLOSED.format(motivo="não consegui resolver a raiz do repositório git a partir do diretório atual"))

    config = os.path.join(raiz, ".gitleaks.toml")
    if not os.path.isfile(config):
        nega(MSG_FAIL_CLOSED.format(motivo=f"config `.gitleaks.toml` ausente na raiz do repositório ({raiz})"))

    # Report em arquivo temporário seguro (mkstemp, modo 0600), apagado no finally.
    fd, report_path = tempfile.mkstemp(prefix="secret-commit-gate-", suffix=".json")
    os.close(fd)
    try:
        try:
            resultado = subprocess.run(
                [
                    "gitleaks",
                    "git",
                    "--pre-commit",
                    "--staged",
                    f"--redact={REDACT}",
                    "--config",
                    config,
                    "--report-format",
                    "json",
                    "--report-path",
                    report_path,
                    "--no-banner",
                    "--log-level",
                    "error",
                    "--exit-code",
                    "1",
                    ".",
                ],
                cwd=raiz,
                capture_output=True,  # saída bruta capturada e NUNCA repassada
                timeout=TIMEOUT_GITLEAKS,
            )
        except FileNotFoundError:
            nega(MSG_FAIL_CLOSED.format(motivo="gitleaks não está no PATH"))
        except subprocess.TimeoutExpired:
            nega(MSG_FAIL_CLOSED.format(motivo=f"a varredura estourou o timeout de {TIMEOUT_GITLEAKS}s"))

        if resultado.returncode == 0:
            return  # limpo: silêncio total, o commit segue

        achados = []
        if resultado.returncode == 1:
            # Exit 1 é "achado" OU erro fatal do gitleaks; o report desambigua.
            try:
                with open(report_path, encoding="utf-8") as f:
                    conteudo = json.load(f)
                if isinstance(conteudo, list):
                    achados = conteudo
            except (OSError, ValueError):
                achados = []
        if achados:
            nega(mensagem_de_achados(achados))
        # Exit != 0 sem achado no report: erro de execução (config inválida,
        # crash). Fail-closed, sem repassar a saída bruta.
        nega(MSG_FAIL_CLOSED.format(motivo=f"o gitleaks falhou (código de saída {resultado.returncode})"))
    finally:
        try:
            os.unlink(report_path)
        except OSError:
            pass


def main():
    try:
        dados = json.load(sys.stdin)
        if dados.get("tool_name") != "Bash":
            return
        comando = (dados.get("tool_input") or {}).get("command") or ""
        if not e_git_commit(comando):
            return  # caminho quente: todo Bash da sessão passa por aqui
        cwd = dados.get("cwd") or os.getcwd()
    except SystemExit:
        raise
    except Exception as e:
        # Entrada ilegível: sem ler o comando não dá pra saber se é commit.
        # O gate prefere bloquear a falhar em silêncio (fail-closed).
        nega(MSG_FAIL_CLOSED.format(motivo=f"entrada do hook ilegível ({type(e).__name__})"))
    try:
        roda_gate(cwd)
    except SystemExit:
        raise
    except Exception as e:
        nega(MSG_FAIL_CLOSED.format(motivo=f"erro interno do gate ({type(e).__name__})"))


if __name__ == "__main__":
    main()
    sys.exit(0)
