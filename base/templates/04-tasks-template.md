# Tarefas — [Nome da fatia]

> Autor: mesa de Desenho
> Baseado em: 03-plan.md

Tarefas pequenas, ordenáveis, cada uma com um único critério de pronto. Cada implementer pega uma por vez.

Este arquivo é o estado durável da fatia. Sessão nova retoma daqui, não da conversa. O box carrega quatro estados, não dois: `[ ]` não começou, `[~]` em execução, `[x]` fechada, `[!]` falhou. No despacho, o último campo do sufixo passa a carregar o rastro, que é perfil, ramo, commit curto e estado: `- [~] T04 — [descrição]. (infra | núcleo | toca: [caminhos] | ramo: sdd/<NNN>/T04)` em execução, `ramo: sdd/<NNN>/T04 @ a1b2c3d` ao fechar em `[x]`, `ramo: sdd/<NNN>/T04, parou em a1b2c3d` ao falhar em `[!]`. Marque a mudança de estado no momento em que ela acontece, nunca depois.

Cada tarefa é uma linha e um único critério de pronto; tarefa composta conta pelo número de critérios. Núcleo: removê-la falha um critério de aceite da spec; sustentação sem motivo é lacuna. Regra anti-inchaço: metadado de tarefa nunca ganha linha própria; a tarefa permanece uma linha, marcadores em sufixo entre parênteses; só `[DONO]` carrega os quatro campos, só sustentação carrega motivo.

Sufixo da tarefa: `(<perfil> | <núcleo|sustentação: motivo> | toca: <caminhos> | <independente|depende de: Txx>)`. O perfil é o primeiro token, sempre, e sai de um vocabulário fechado: `texto | front | back | infra`. Ele roteia o despacho e a carga de insumo do implementer; ele acrescenta, nunca dispensa item do piso nem substitui o checklist, que mora em `implementer.md`. Perfil não tem default: tarefa sem perfil, ou com palavra fora do vocabulário, bloqueia o despacho dela mesma, nomeada, e as demais seguem.

`toca:` declara os caminhos que a tarefa edita, e é essa declaração que torna a independência falseável: o condutor cruza as superfícies por ferramenta antes de despachar, e duas tarefas só rodam juntas com superfícies disjuntas. Serial é o default; omissão, dúvida ou superfície não disjunta significa serial. O interlock dispara pela matéria tocada, nunca pelo rótulo: declaração `toca:` que cruze `.gitleaks.toml`, `.github/workflows/`, `.claude/settings.json`, `.claude/hooks/` ou `hooks/` serializa sozinha, em qualquer perfil, e nunca é marcada `independente`. Os arquivos do caminho de enforcement formam um conjunto único: serem arquivos diferentes não os torna superfícies disjuntas.

- [ ] T01 — [descrição]. Pronto quando: [critério]. (texto | núcleo | toca: [caminhos] | independente)
- [ ] T02 — [descrição]. Pronto quando: [critério]. (back | sustentação: [a triagem que a exige ou o cartão de padrão que a manda] | toca: [caminhos] | depende de: T01)
- [ ] T03 — [DONO] [o quê em uma linha]. Pronto quando: [critério]. (quando: [momento, fora do caminho crítico] | bloqueia: [o que espera por ela] | duração: [estimativa] | independente)

## Ordem e dependências

Qual tarefa depende de qual. Tarefa `[DONO]` fica fora do caminho crítico; no caminho crítico só com aceite explícito do dono na mensagem do portão de Desenho.

## Disciplinas embutidas

As tarefas de segurança, experiência e deploy fazem parte da fatia, não são anexo. Toda tabela com dado pessoal já vem com migration e política de acesso no mesmo passo. A tela já vem com seus estados de carregando, vazio e erro. Tarefa de front em superfície rica compara o screenshot do resultado com o moodboard antes de fechar e registra a comparação. O deploy já vem com rollback. Fatia que cria ou estende módulo atualiza `specs/_arquitetura/mapa-do-sistema.md` no mesmo passo, nunca depois. Não existe tarefa de "segurança depois".
