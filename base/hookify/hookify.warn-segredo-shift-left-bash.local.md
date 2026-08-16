---
name: warn-segredo-shift-left-bash
enabled: true
event: bash
action: warn
conditions:
  - field: command
    operator: regex_match
    pattern: \bAKIA[0-9A-Z]{16}\b|\bghp_[A-Za-z0-9]{36,}|\bsk-[A-Za-z0-9_-]{20,}|-{5}BEGIN [A-Z ]*PRIVATE KEY-{5}
  - field: command
    operator: not_contains
    pattern: framework/hooks/test/corpus/
---

Aviso (heurística): o texto contém um padrão que parece segredo (chave AWS `AKIA…`, token GitHub `ghp_…`, chave `sk-…` ou bloco PEM de chave privada). A detecção é regex simples, sem entropia e sem allowlist: pode ser falso positivo.

Regra: constituição, seção "O que nunca fazer" ("Nunca colocar segredo no repositório") e seção "Regras de domínio e privacidade" (segredo em variável de ambiente, nunca no código).

Caminho: o segredo sai do código e vai pra variável de ambiente; a chave se documenta no `.env.example`, nunca o valor. Falso positivo entra no `.gitleaks.toml` via PR (allowlist versionada, path exato). Esta é a camada de aviso na escrita: o gate de commit roda gitleaks e bloqueia; a varredura no CI é a linha autoritativa.
