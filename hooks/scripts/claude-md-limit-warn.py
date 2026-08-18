#!/usr/bin/env python3
"""Hook PostToolUse (Write|Edit): teto de 120 linhas do CLAUDE.md.

Aviso, fail-open. Este hook roda DEPOIS da escrita (PostToolUse): a
ferramenta já gravou o arquivo e não há como desfazer daqui. Bloquear
não teria efeito, por isso o script sempre sai com exit 0. Erro interno
(JSON malformado no stdin, arquivo sumiu do disco, encoding inesperado)
também sai com exit 0 em silêncio: um hook de aviso nunca derruba a
sessão de quem trabalha.

Comportamento:
- Lê o payload JSON do hook no stdin e extrai tool_input.file_path.
- Só age quando o nome do arquivo é exatamente `CLAUDE.md` (case exato,
  qualquer diretório).
- Conta as linhas do arquivo no disco. Acima de 120, emite o aviso do
  catálogo (hooks/mensagens.md, seção 5) com "N/120".
- Em qualquer outro caso, silêncio total.

Somente stdlib do Python 3. Texto da mensagem: fonte única em
hooks/mensagens.md.
"""

import json
import os
import sys

LIMITE = 120

MENSAGEM = (
    "Aviso: `CLAUDE.md` está com {n}/{limite} linhas.\n"
    "\n"
    "Regra: constituição, seção \"Engenharia de contexto e harness\" "
    "(item 1, teto de 120 linhas) e seção \"O que nunca fazer\" "
    "(\"Nunca deixar esta constituição passar de 120 linhas\").\n"
    "\n"
    "Caminho: mova o conteúdo novo para `docs/` e deixe no `CLAUDE.md` "
    "só a referência."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        file_path = payload.get("tool_input", {}).get("file_path", "")
        if not isinstance(file_path, str) or not file_path:
            return 0
        if os.path.basename(file_path) != "CLAUDE.md":
            return 0
        with open(file_path, encoding="utf-8", errors="replace") as f:
            n = len(f.read().splitlines())
        if n > LIMITE:
            print(MENSAGEM.format(n=n, limite=LIMITE))
        return 0
    except Exception:
        # Fail-open silencioso: aviso nunca bloqueia nem vaza stack trace.
        return 0


if __name__ == "__main__":
    sys.exit(main())
