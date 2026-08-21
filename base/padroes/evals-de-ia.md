# Cartão de padrão — Evals de IA

> Consulte quando a fatia tem LLM em runtime: geração, RAG, classificação, agente embutido no produto.
> Base: AI Engineering (Chip Huyen), Generative AI Design Patterns. A teoria fica com o modelo; aqui é a nossa posição.
> Versão: 1.0 · Revisado: 2026-08-20 · Gatilho de revisão: release do plugin

## Contexto

Feature de IA não é determinística. Teste tradicional cobre o contrato, não a qualidade da saída. Sem avaliação sistemática, regressão de prompt e de modelo passam invisíveis.

## Nosso padrão

- Toda fatia com LLM em runtime nasce com um golden set: casos de entrada e saída esperada, versionado no repo junto da fatia (`specs/NNN-*/evals/`). Começa pequeno (10 a 20 casos), cresce com os erros reais de produção.
- A avaliação roda no CI: asserts determinísticos onde der (formato, campos, limites) e LLM-as-judge para qualidade subjetiva, com rubrica escrita.
- Prompt é artefato versionado, nunca string solta no código. Mudança de prompt ou de modelo roda os evals antes do merge, como qualquer teste.
- A mesa de Desenho define a métrica de aceite da feature (taxa de acerto no golden set, ou a métrica que o caso pedir) e ela entra nos critérios de aceite da spec.

## Proibido

- Subir feature de IA sem golden set.
- "Testei na mão e funcionou" como veredito. Evidência é resultado de eval, não anedota.
- Trocar prompt ou modelo sem rodar os evals.

## Exige nota de decisão

- Troca de modelo ou provider.
- Fine-tuning (antes dele: prompt e RAG esgotados?).
