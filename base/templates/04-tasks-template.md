# Tarefas — [Nome da fatia]

> Autor: mesa de Desenho
> Baseado em: 03-plan.md

Tarefas pequenas, ordenáveis, cada uma com critério de pronto. O implementer pega uma por vez.

Este arquivo é o estado durável da fatia. Sessão nova retoma daqui, não da conversa. Marque o checkbox no momento em que a tarefa fecha.

- [ ] T01 — [descrição]. Pronto quando: [critério].
- [ ] T02 — [descrição]. Pronto quando: [critério].
- [ ] T03 — ...

## Ordem e dependências

Qual tarefa depende de qual.

## Disciplinas embutidas

As tarefas de segurança, experiência e deploy fazem parte da fatia, não são anexo. Toda tabela com dado pessoal já vem com migration e política de acesso no mesmo passo. A tela já vem com seus estados de carregando, vazio e erro. O deploy já vem com rollback. Fatia que cria ou estende módulo atualiza `specs/_arquitetura/mapa-do-sistema.md` no mesmo passo, nunca depois. Não existe tarefa de "segurança depois".
