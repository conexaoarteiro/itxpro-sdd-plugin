#!/usr/bin/env python3
"""Hook PreToolUse (Write/Edit): aviso de implementação sem spec aprovada.

Regra da fatia 001 (plano, seção "Contratos"): escrita de código sem nenhuma
spec aprovada gera AVISO, não bloqueio (decisão do portão de Intenção, v1).
Fail-open por decisão do plano: erro interno nunca bloqueia a ferramenta.

Gatilho de "implementação" (versionado aqui, junto à regra):
  - extensão do arquivo na lista EXTENSOES_DE_CODIGO; E
  - path fora dos diretórios de PATHS_EXCLUIDOS (specs/, docs/, .claude/,
    .github/, framework, _templates). A exclusão vale para qualquer
    segmento do path relativo à raiz do projeto: escolha conservadora que
    prefere silêncio a falso positivo, coerente com o modo fail-open.

Contrato de "spec aprovada" (portão de Intenção, Q1): existe ao menos um
`specs/NNN-*/01-spec.md` com a linha literal `Status: aprovada`. O template de
spec escreve os metadados em blockquote, então a linha vale com ou sem o
prefixo `> ` (`> Status: aprovada` conta como aprovada).

RISCO DE FALSO NEGATIVO DOMINANTE (reconhecido no plano): a checagem
"existe alguma spec aprovada" silencia para sempre depois da PRIMEIRA
aprovação do projeto. Código da fatia 007 escrito sob a spec da fatia 001
não dispara nada. O mapeamento arquivo→fatia é pré-condição nomeada do
endurecimento e não existe na v1.

CONDIÇÃO DE ENDURECIMENTO (mensurável): cada disparo appenda uma linha no
log do hook. A regra endurece de aviso para bloqueio após N disparos
revisados com taxa de falso positivo ~zero. Sem log não há métrica.

LUGAR DO LOG (fatia 012): fora da árvore do projeto, no diretório git do
clone, em `$(git rev-parse --git-common-dir)/itxpro-sdd/hooks-log.jsonl`,
com o comando resolvido a partir da raiz do projeto (`git -C <raiz>`); em
worktree é o `.git` principal, então um clone tem um log só. O git nunca
indexa nada sob o próprio diretório. Sem diretório git resolvível a partir
da raiz (projeto sem repositório, git ausente ou que não responde em
TIMEOUT_GIT, escrita recusada) nada é gravado, em lugar nenhum, e a
mensagem diz isso. O hook nunca escreve na árvore do projeto, com ou sem
git, e nunca abre o arquivo antigo das versões 0.1.0 a 0.8.0.

O QUE A LINHA CARREGA: {"regra", "timestamp", "path"}, e `path` tem três
formas: caminho POSIX relativo à raiz (`src/api.ts`); o marcador
`fora-da-raiz` para arquivo fora da raiz, sem nenhum segmento do caminho;
`erro-interno: <tipo da exceção>` no ramo de erro. Promessa da linha:
nunca conteúdo de arquivo, nunca dado da máquina (caminho absoluto,
diretório home, nome de usuário).

Mecanismo de aviso: exit 0 + JSON em stdout com o campo `systemMessage`.
Escolha documentada: em PreToolUse, exit 2 bloqueia a ferramenta (proibido
aqui, o modo é aviso) e a saída de erro com exit 0 só aparece em modo
debug, ou seja, o aviso morreria invisível. O `systemMessage` do formato
JSON de saída de hooks exibe a mensagem sem decidir permissão: não bloqueia.
Texto da mensagem: catálogo `hooks/mensagens.md`, seção 4.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Lista de extensões que contam como "implementação" (plano, gatilho).
EXTENSOES_DE_CODIGO = {".ts", ".tsx", ".js", ".jsx", ".py", ".sql", ".go", ".rs", ".css"}

# Diretórios fora do gatilho (plano, gatilho).
PATHS_EXCLUIDOS = {"specs", "docs", ".claude", ".github", "framework", "_templates"}

# Linha que encerra o aviso, com prefixo de blockquote opcional.
RE_APROVADA = re.compile(r"^\s*(>\s*)?Status:\s*aprovada\s*$")

# Diretórios de spec: specs/NNN-*/01-spec.md.
RE_FATIA = re.compile(r"^\d{3}-")

# Lugar do log, sob o diretório git do clone (fatia 012, plano C1).
SUBDIR_LOG = ("itxpro-sdd", "hooks-log.jsonl")

# Rótulo gravado quando o arquivo está fora da raiz: nenhum segmento do caminho.
MARCADOR_FORA_DA_RAIZ = "fora-da-raiz"

# Orçamento: o hook de arquivo tem 300 ms na suíte (ORCAMENTO_ARQUIVO, plano da 001); interpretador e resto do hook custam até 43 ms de cota superior (M8); 200 ms deixa margem para o TimeoutExpired, que chega em 206 ms (M17), e para a variação do runner; é 13x a mediana medida da chamada (M4). Git travado cai no fallback e nunca segura o editor (RS-15).
TIMEOUT_GIT = 0.200  # segundos

_PREFIXO = (
    "Aviso: escrita de código em `{arquivo}` sem nenhuma spec aprovada "
    "(nenhum `specs/*/01-spec.md` com a linha `Status: aprovada`).\n\n"
    'Regra: constituição, seção "O que nunca fazer" '
    '("Nunca começar uma fatia sem spec aprovada em `specs/`").\n\n'
    "Caminho: leve a fatia à mesa de Intenção e aprove a spec no portão "
    "humano; a linha `Status: aprovada` no `01-spec.md` encerra o aviso. "
)

MENSAGEM = _PREFIXO + (
    "Este disparo ficou registrado fora da árvore do projeto, no diretório "
    "git do clone: `$(git rev-parse --git-common-dir)/itxpro-sdd/hooks-log.jsonl` "
    "(regra, timestamp e caminho relativo à raiz do projeto, ou o marcador "
    "`fora-da-raiz`; nunca conteúdo de arquivo, nunca dado da máquina: "
    "caminho absoluto, diretório home ou nome de usuário)."
)

MENSAGEM_SEM_REGISTRO = _PREFIXO + (
    "Este disparo não ficou registrado: o hook grava só no diretório git do "
    "clone (`git rev-parse --git-common-dir`), que não resolveu a partir da "
    "raiz do projeto ou não aceitou a escrita, e ele nunca grava na árvore "
    "do projeto."
)


def raiz_do_projeto(dados):
    """Raiz do projeto: CLAUDE_PROJECT_DIR (setado pelo Claude Code), senão o cwd do hook."""
    raiz = os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or os.getcwd()
    return Path(raiz)


def caminho_relativo(file_path, raiz):
    """Caminho POSIX do arquivo relativo à raiz, resolvido (symlink, entrada
    relativa e `..` interno); None se o arquivo está fora da raiz."""
    caminho = Path(file_path)
    absoluto = caminho if caminho.is_absolute() else raiz / caminho
    try:
        return absoluto.resolve().relative_to(raiz.resolve()).as_posix()
    except ValueError:
        return None


def e_implementacao(file_path, raiz):
    """True se o path dispara o gatilho: extensão de código e fora dos paths excluídos."""
    caminho = Path(file_path)
    if caminho.suffix.lower() not in EXTENSOES_DE_CODIGO:
        return False
    relativo = caminho_relativo(file_path, raiz)
    # Fora da raiz do projeto: avalia os segmentos do próprio path.
    partes = Path(relativo).parts if relativo is not None else caminho.parts
    return not any(parte in PATHS_EXCLUIDOS for parte in partes)


def existe_spec_aprovada(raiz):
    """True se algum specs/NNN-*/01-spec.md tem a linha `Status: aprovada`."""
    for spec in raiz.glob("specs/*/01-spec.md"):
        if not RE_FATIA.match(spec.parent.name):
            continue
        try:
            with open(spec, encoding="utf-8", errors="replace") as f:
                for linha in f:
                    if RE_APROVADA.match(linha):
                        return True
        except OSError:
            continue
    return False


def diretorio_git(raiz):
    """Diretório git comum do clone, resolvido a partir da raiz (RS-15); None
    quando não há. Chamada em lista, sem shell, entrada e saída de erro
    descartadas, sem prompt e sem lock opcional; check desligado porque a
    exceção do check carrega a linha de comando com a raiz absoluta. O
    resultado só vale com exit 0, uma linha não vazia e um diretório que
    contém HEAD. Git ausente, timeout e valor inválido viram None, nunca
    erro interno. O caminho resolvido serve só para abrir o arquivo: nunca
    vai a log, stdout ou mensagem."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(raiz), "rev-parse", "--git-common-dir"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
            timeout=TIMEOUT_GIT,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"},
        )
        if proc.returncode != 0:
            return None
        saida = proc.stdout.strip()
        if not saida or "\n" in saida:
            return None
        comum = (raiz / saida).resolve()
        if not (comum.is_dir() and (comum / "HEAD").is_file()):
            return None
        return comum
    except Exception:
        # OSError (git ausente), SubprocessError (timeout), ValueError: sem lugar.
        return None


def registra_disparo(raiz, rotulo):
    """Appenda o disparo no log sob o diretório git do clone. Devolve True se
    gravou; False sem diretório git ou em qualquer falha (fail-open total).
    Nunca cria nem edita arquivo na árvore do projeto."""
    try:
        comum = diretorio_git(raiz)
        if comum is None:
            return False
        log = comum.joinpath(*SUBDIR_LOG)
        log.parent.mkdir(parents=True, exist_ok=True)
        linha = {
            "regra": "spec-approval-warn",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": rotulo,
        }
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
        return True
    except Exception:
        return False


def main():
    dados = json.load(sys.stdin)
    if dados.get("tool_name") not in ("Write", "Edit"):
        return
    file_path = (dados.get("tool_input") or {}).get("file_path")
    if not file_path:
        return
    raiz = raiz_do_projeto(dados)
    if not e_implementacao(file_path, raiz):
        return
    if existe_spec_aprovada(raiz):
        return
    relativo = caminho_relativo(file_path, raiz)
    registrado = registra_disparo(raiz, relativo if relativo is not None else MARCADOR_FORA_DA_RAIZ)
    texto = MENSAGEM if registrado else MENSAGEM_SEM_REGISTRO
    print(json.dumps({"systemMessage": texto.format(arquivo=file_path)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Fail-open por decisão do plano: erro interno não bloqueia.
        # Registra no log quando possível, para o erro não ser silencioso:
        # só o tipo da exceção, nunca a mensagem dela (RS-3).
        try:
            registra_disparo(Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()), f"erro-interno: {type(e).__name__}")
        except Exception:
            pass
    sys.exit(0)
