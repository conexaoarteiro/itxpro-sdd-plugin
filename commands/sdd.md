---
description: Conduz o pipeline SDD do projeto. Sem constituição, aponta o setup; com constituição fechada, invoca o condutor.
argument-hint: [fatia ou instrução para o condutor]
---

# /sdd — despachante do pipeline SDD

Você é um despachante fino. Você não conduz mesa, não faz entrevista e não implementa: você detecta o estado do projeto e aciona a skill certa. Fixe `export LC_ALL=en_US.UTF-8` antes dos comandos abaixo.

## Cabeçalho, sempre

Leia o campo `version` de `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`. Toda resposta deste comando abre com a versão instalada: `itxpro-sdd@X.Y.Z`.

## Detecção de estado, nesta ordem

1. **Não existe `CLAUDE.md` na raiz do projeto**, ou **existe e `grep -qF '[[LACUNA:' CLAUDE.md` encontra lacuna** → o projeto ainda não tem constituição fechada. Responda com o cartão de três linhas e pare. Isso nunca é erro:

   > itxpro-sdd@X.Y.Z
   > Estado: sem constituição (ou: constituição com N lacunas abertas).
   > Próximo passo: rode a skill `sdd-setup` para a entrevista de setup.

2. **`CLAUDE.md` existe e não tem `[[LACUNA:`** → constituição fechada. Antes de qualquer mesa:

   - Conte as pendências: `grep -cE 'PENDENTE:[a-z0-9-]+' CLAUDE.md`. Se houver, avise agora, nunca no meio da mesa: "N pendências abertas na constituição (enumere os ids com a pergunta ao lado, lida do registro da entrevista em `docs/decisoes/*-setup-sdd.md`). Elas não bloqueiam; revise com a skill sdd-setup quando quiser." Fallback: se o registro não existe, mostre só o id e aponte a skill `sdd-setup`; nunca improvise a pergunta. É ritmo, não bloqueio.
   - Compare a versão da linha de origem com a instalada. Leia a versão da linha com a regex ancorada `itxpro-sdd@[0-9]+\.[0-9]+\.[0-9]+` (nunca pegue pontuação vizinha: a linha pode terminar em ponto). Divergência gera um aviso de uma linha ("constituição nascida em X.Y.Z, plugin instalado em A.B.C") e nada mais. Não bloqueie e não reescreva a linha: ela registra nascimento, não versão corrente.
   - Invoque a skill `sdd-conductor`, repassando os argumentos do comando: $ARGUMENTS

## Abertura com constituição fechada

A primeira mensagem mostra, nesta ordem: a versão instalada, a fatia corrente (pelo disco, `specs/NNN-*/`), a fase (pela tabela de estado da skill do condutor) e uma única próxima ação. Uma ação, não um menu.
