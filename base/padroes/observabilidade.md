# Cartão de padrão — Observabilidade

> Consulte na mesa de Desenho de toda fatia que sobe para produção. Dono: devsecops.
> Base: Observability Engineering, Designing Data-Intensive Applications. A teoria fica com o modelo; aqui é a nossa posição.

## Contexto

A constituição pede "observabilidade mínima". Este cartão define o que mínimo significa, para que debugar produção não dependa de adivinhar.

## Nosso padrão

- Evento estruturado (JSON), não linha de log solta. Código novo emite eventos com contexto rico: `request_id`, rota, papel do usuário, duração, resultado. Nunca dado pessoal (regra constitucional).
- Alta cardinalidade é bem-vinda: `request_id` e identificadores técnicos permitem perguntar "o que aconteceu com ESTA requisição". Um `request_id` atravessa app, Supabase e integração externa.
- Cada fatia declara seu SLO no plano: disponibilidade do fluxo principal e o p95 já exigido pelo orçamento de desempenho. O SLO é a fronteira entre "ruim mas tolerável" e "acorda alguém".
- Alerta só sobre sintoma do usuário (SLO violado, fluxo principal quebrado), nunca sobre causa interna (CPU, memória). Todo alerta tem ação definida; alerta sem ação é ruído e morre.
- Baseline da fatia 1 de qualquer projeto: eventos estruturados da app, logs da Supabase, check de disponibilidade externo.

## Proibido

- Dado pessoal em evento, log ou telemetria.
- Log não estruturado em código novo.
- Alerta sem ação definida no runbook da fatia.

## Exige nota de decisão

- Ferramenta de observabilidade nova (APM, tracing distribuído). Começamos com o que a plataforma dá; ferramenta entra quando a dor justificar.
