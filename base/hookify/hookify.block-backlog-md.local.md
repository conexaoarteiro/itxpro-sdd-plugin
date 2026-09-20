---
name: block-backlog-md
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: (?i)(^|/)backlog\.md$
---

Bloqueado: tentativa de escrever `backlog.md`. Backlog não vive em markdown neste repositório.

Regra: constituição, seção "O que nunca fazer" ("Nunca manter backlog em markdown no repo") e seção "Gestão de trabalho", onde mora a regra da label de prioridade da issue.

Caminho: registre a demanda como issue, já com a label que aquela regra pede, e consulte sob demanda:

`gh issue create --title "resumo da demanda" --label P1`

`gh issue list --label P0`
