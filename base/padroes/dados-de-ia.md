# Cartão de padrão — Dados de IA

> Consulte quando a fatia vetoriza dado, envia dado a provider de modelo, ou monta dataset (golden set, exemplos few-shot).
> Base: AI Engineering, Data Governance, Designing Data-Intensive Applications. A teoria fica com o modelo; aqui é a nossa posição.
> Versão: 1.0 · Revisado: 2026-08-20 · Gatilho de revisão: release do plugin

## Contexto

Dado que alimenta IA continua sendo dado. Vetorização e envio a provider criam cópias derivadas que escapam do controle de acesso se não forem tratadas como o original. Para uma empresa de GRC TI, essa é uma posição de reputação, não só técnica.

## Nosso padrão

- Vetor vive no mesmo banco transacional do projeto, com a extensão vetorial que a stack declarada oferece; sem banco vetorial dedicado. O índice vetorial entra no plano de índice do orçamento de desempenho, como qualquer índice.
- Embedding de dado pessoal é dado pessoal. Herda a classificação da fonte, mora em tabela com a mesma política de acesso da fonte, e entra no apagamento: quando o titular pede exclusão, o vetor derivado morre junto.
- Envio a provider de modelo é transferência a terceiro. Minimização (só o necessário da tarefa), base legal clara (LGPD), e preferência por provider e modalidade com zero data retention. O plano da fatia registra o que é enviado a quem.
- Golden set e exemplos few-shot com dado real são anonimizados antes de entrar no repo. Dataset versionado é código: passa pela mesma revisão.

## Proibido

- Vetorizar dado pessoal em tabela sem política de acesso.
- Enviar dado de usuário a provider sem base legal e minimização.
- Dado pessoal cru em golden set ou exemplo versionado.

## Exige nota de decisão

- Banco vetorial dedicado (a dor de escala precisa existir e estar medida).
- Fine-tuning com dado de usuário.
- Provider de modelo novo ou mudança de modalidade de retenção.
