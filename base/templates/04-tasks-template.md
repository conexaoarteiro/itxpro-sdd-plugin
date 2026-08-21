# Tarefas — [Nome da fatia]

> Autor: mesa de Desenho
> Baseado em: 03-plan.md

Tarefas pequenas, ordenáveis, cada uma com um único critério de pronto. Cada implementer pega uma por vez.

Este arquivo é o estado durável da fatia. Sessão nova retoma daqui, não da conversa. Marque o checkbox no momento em que a tarefa fecha.

Cada tarefa é uma linha e um único critério de pronto; tarefa composta conta pelo número de critérios. Núcleo: removê-la falha um critério de aceite da spec; sustentação sem motivo é lacuna. A marcação de independência é declarativa e dormente até a issue #40. Regra anti-inchaço: metadado de tarefa nunca ganha linha própria; a tarefa permanece uma linha, marcadores em sufixo entre parênteses; só `[DONO]` carrega os quatro campos, só sustentação carrega motivo.

- [ ] T01 — [descrição]. Pronto quando: [critério]. (núcleo | independente)
- [ ] T02 — [descrição]. Pronto quando: [critério]. (sustentação: [a triagem que a exige ou o cartão de padrão que a manda] | depende de: T01)
- [ ] T03 — [DONO] [o quê em uma linha]. Pronto quando: [critério]. (quando: [momento, fora do caminho crítico] | bloqueia: [o que espera por ela] | duração: [estimativa] | independente)

## Ordem e dependências

Qual tarefa depende de qual. Tarefa `[DONO]` fica fora do caminho crítico; no caminho crítico só com aceite explícito do dono na mensagem do portão de Desenho.

## Disciplinas embutidas

As tarefas de segurança, experiência e deploy fazem parte da fatia, não são anexo. Toda tabela com dado pessoal já vem com migration e política de acesso no mesmo passo. A tela já vem com seus estados de carregando, vazio e erro. Tarefa de front em superfície rica compara o screenshot do resultado com o moodboard antes de fechar e registra a comparação. O deploy já vem com rollback. Fatia que cria ou estende módulo atualiza `specs/_arquitetura/mapa-do-sistema.md` no mesmo passo, nunca depois. Não existe tarefa de "segurança depois".
