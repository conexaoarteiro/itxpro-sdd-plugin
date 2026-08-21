# Cartão de padrão — Fundação: CI base

> Herdado no setup do projeto; consulte na mesa de Desenho antes de criar qualquer tarefa de CI. O plano declara só o delta.
> Versão: 1.0 · Revisado: 2026-08-20 · Gatilho de revisão: release do plugin · Dono: devsecops

## Contexto

CI é fundação do projeto, não tarefa de fatia. Plano que reconstrói pipeline paga duas vezes: em horas na mesa e em deriva entre fatias. Este cartão fixa o mínimo que todo projeto herda e mantém.

## Nosso padrão

- Um workflow de CI desde a primeira fatia com código: lint, build, teste e varredura de segredo, e a falha de qualquer passo bloqueia o job.
- Gatilho duplo: `pull_request` e `push` no branch padrão.
- Actions pinadas por SHA de commit, nunca por tag mutável; atualizar um pin é PR normal.
- Esqueleto colável (a varredura de segredo vive no workflow herdado, cartão `gitleaks.md`):

```yaml
on:
  push:
    branches: [<branch padrão>]
  pull_request:
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha-pinado>
      - run: <lint>
      - run: <build>
      - run: <teste>
```

## Proibido

- Tarefa de fatia que recria item do CI herdado; o delta (job novo, budget novo) entra no plano, o pipeline não.
- Action sem pin de SHA.
- Desligar lint, teste ou varredura para o CI passar.

## Exige nota de decisão

- Trocar a plataforma de CI ou criar pipeline paralelo.

## Como verificar herança

- Arquivo: o workflow de CI em `.github/workflows/` do projeto.
- Comando: `ls .github/workflows/` mostra o workflow; `gh run list --limit 1` mostra o último run do branch padrão verde.
