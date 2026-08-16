#!/usr/bin/env python3
"""Hook PreToolUse (Write/Edit): aviso de implementação sem spec aprovada.

Regra da fatia 001 (plano, seção "Contratos"): escrita de código sem nenhuma
spec aprovada gera AVISO, não bloqueio (decisão do portão de Intenção, v1).
Fail-open por decisão do plano: erro interno nunca bloqueia a ferramenta.

Gatilho de "implementação" (versionado aqui, junto à regra):
  - extensão do arquivo na lista EXTENSOES_DE_CODIGO; E
  - path fora dos diretórios de PATHS_EXCLUIDOS (specs/, docs/, .claude/,
    .github/, framework/, _templates/). A exclusão vale para qualquer
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

CONDIÇÃO DE ENDURECIMENTO (mensurável): cada disparo appenda uma linha em
`.claude/hooks-log.jsonl` ({"regra", "timestamp", "path"}, nunca conteúdo
de arquivo). A regra endurece de aviso para bloqueio após N disparos
revisados com taxa de falso positivo ~zero. Sem log não há métrica.

Mecanismo de aviso: exit 0 + JSON em stdout com o campo `systemMessage`.
Escolha documentada: em PreToolUse, exit 2 bloqueia a ferramenta (proibido
aqui, o modo é aviso) e stderr com exit 0 só aparece em modo debug, ou
seja, o aviso morreria invisível. O `systemMessage` do formato JSON de
saída de hooks exibe a mensagem sem decidir permissão: não bloqueia.
Texto da mensagem: catálogo `framework/hooks/mensagens.md`, seção 4.
"""

import json
import os
import re
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

MENSAGEM = (
    "Aviso: escrita de código em `{arquivo}` sem nenhuma spec aprovada "
    "(nenhum `specs/*/01-spec.md` com a linha `Status: aprovada`).\n\n"
    'Regra: constituição, seção "O que nunca fazer" '
    '("Nunca começar uma fatia sem spec aprovada em `specs/`").\n\n'
    "Caminho: leve a fatia à mesa de Intenção e aprove a spec no portão "
    "humano; a linha `Status: aprovada` no `01-spec.md` encerra o aviso. "
    "Este disparo ficou registrado em `.claude/hooks-log.jsonl` "
    "(regra, timestamp e path, nunca conteúdo)."
)


def raiz_do_projeto(dados):
    """Raiz do projeto: CLAUDE_PROJECT_DIR (setado pelo Claude Code), senão o cwd do hook."""
    raiz = os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or os.getcwd()
    return Path(raiz)


def e_implementacao(file_path, raiz):
    """True se o path dispara o gatilho: extensão de código e fora dos paths excluídos."""
    caminho = Path(file_path)
    if caminho.suffix.lower() not in EXTENSOES_DE_CODIGO:
        return False
    try:
        relativo = (raiz / caminho).resolve().relative_to(raiz.resolve()) if not caminho.is_absolute() else caminho.resolve().relative_to(raiz.resolve())
    except ValueError:
        # Fora da raiz do projeto: avalia os segmentos do próprio path.
        relativo = caminho
    return not any(parte in PATHS_EXCLUIDOS for parte in relativo.parts)


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


def registra_disparo(raiz, file_path):
    """Appenda o disparo no log. Falha de log não quebra o hook (fail-open total)."""
    try:
        log = raiz / ".claude" / "hooks-log.jsonl"
        log.parent.mkdir(parents=True, exist_ok=True)
        linha = {
            "regra": "spec-approval-warn",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": str(file_path),
        }
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    except Exception:
        pass


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
    registra_disparo(raiz, file_path)
    print(json.dumps({"systemMessage": MENSAGEM.format(arquivo=file_path)}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Fail-open por decisão do plano: erro interno não bloqueia.
        # Registra no log quando possível, para o erro não ser silencioso.
        try:
            registra_disparo(Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()), f"erro-interno: {type(e).__name__}")
        except Exception:
            pass
    sys.exit(0)
