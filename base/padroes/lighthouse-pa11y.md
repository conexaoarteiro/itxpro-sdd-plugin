# Cartão de padrão — Fundação: auditoria de desempenho e acessibilidade

> Herdado no setup; consulte na mesa de Desenho de toda fatia que toca UI. O plano declara só o delta de budget.
> Versão: 1.0 · Revisado: 2026-08-20 · Gatilho de revisão: release do plugin · Dono: ux-architect

## Contexto

Qualidade percebida e acessibilidade regridem em silêncio quando não têm gate. O orçamento de desempenho do plano precisa de régua automática no CI, não de impressão de quem revisa.

## Nosso padrão

- Lighthouse CI com budget versionado no repo. O orçamento é o do plano da fatia (Core Web Vitals alvo); sem plano dizendo diferente, vale o default: performance ≥ 90 e acessibilidade ≥ 90 na página principal.
- pa11y (ou equivalente) contra WCAG 2.1 AA nas páginas novas ou alteradas.
- Gatilho: PR que toca UI. PR sem UI não paga esse job.
- Resultado é gate: budget estourado ou violação AA falha o job. A exceção sobe ao plano da fatia, nunca se ajusta o budget dentro do PR.

## Proibido

- Ajustar o budget no mesmo PR que o estourou.
- Marcar violação AA como conhecida sem registro no plano da fatia.
- Tarefa de fatia que recria a auditoria herdada; o plano declara só o delta.

## Exige nota de decisão

- Baixar o orçamento default do projeto.

## Como verificar herança

- Arquivo: o workflow de auditoria e o arquivo de budget versionados no repo do projeto.
- Comando: `gh run list --limit 5` mostra o job de auditoria verde no último PR que tocou UI.
