---
name: block-backlog-md-bash
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: (?i)\btouch\b[^;&|>]*[\s/'"]backlog\.md(\s|$|['";&|])|>>?\s*['"]?([^\s;&|]*/)?backlog\.md(\s|$|['";&|])|\b(?:cp|mv)\b[^;&|>]*[\s/'"]backlog\.md['"]?\s*($|[;&|])
---

Bloqueado: tentativa de escrever `backlog.md`. Backlog não vive em markdown neste repositório.

Regra: constituição, seção "O que nunca fazer" ("Nunca manter backlog em markdown no repo") e seção "Gestão de trabalho".

Caminho: registre a demanda como issue e consulte sob demanda:

`gh issue create --title "resumo da demanda" --label P1`

`gh issue list --label P0`
