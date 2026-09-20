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

Depois da próxima ação, dois complementos:

- **Aviso de branch à frente**, medido antes de concluir. Rode o fence de "Medida do branch à frente" e imprima a linha que ele devolver, sem recompor. Ele lê o remoto com uma chamada só, `git ls-remote --symref origin HEAD`, que traz o branch padrão e o sha na mesma resposta e não escreve ref nenhuma, e responde as duas direções contadas em `specs/`: quanto este branch está à frente do publicado e quanto está atrás. O que essa leitura não responder sai nomeado como não medido, em uma linha, com o mesmo peso do caminho feliz. Sem linha nenhuma, não há o que avisar. Nunca conclua sobre o remoto por `refs/remotes/origin/HEAD` nem por contagem contra `origin/<padrão>`: essas refs são a visão do último `fetch`, e afirmar a partir delas é afirmar mais do que se mediu. Só nome de branch, contagem e `specs/`: nunca URL de remoto, caminho absoluto ou saída bruta de git.
- **Rodapé de feedback**, sempre, uma linha: "Lacuna do framework? Abra issue em https://github.com/conexaoarteiro/itxpro-sdd-plugin/issues (pública: sem segredo, log bruto, .env nem dado pessoal; descreva por categoria e cite itxpro-sdd@X.Y.Z)."

## Aviso de branch à frente

O comando abaixo é o aviso: ele mede e devolve a linha pronta. A suíte do framework o extrai pelo cabeçalho fixo "Medida do branch à frente" e o executa em repositório temporário, então mudar o texto sem o bloco quebra o teste. Códigos de saída, casa única: **0** medido, **74** o commit publicado não está no meu disco, **70** não medi. Em 70 e em 74 a linha sai mesmo assim, nomeando o que ficou sem resposta.

### Medida do branch à frente

```bash
# Aviso de branch à frente do despachante /sdd (fatia 013, CA32).
# O remoto se mede ANTES de concluir, com UMA leitura que não escreve:
# `git ls-remote --symref origin HEAD` traz o branch padrão e o sha do publicado
# na mesma resposta. `git fetch` e `git remote set-head` estão fora daqui: os
# dois escrevem ref no repositório de quem só abriu o comando. A visão local do
# remoto também está fora, porque ela é o retrato do último fetch, e concluir
# dela é afirmar mais do que se mediu. O que a leitura não responde sai nomeado.
# Saída: a linha do aviso, pronta para imprimir, com as duas direções contadas
# em specs/; nenhuma linha quando não há o que avisar. Sem URL de remoto, sem
# caminho absoluto e sem saída bruta de git (RS-6).
# 0 medido | 74 o publicado não está no meu disco | 70 não medi.
RESSALVA='; o estado da fatia só existe neste branch até o fechamento de fase integrar e publicar.'
nao_medi() {   # <motivo>: a linha de não medido tem o peso do caminho feliz
  printf 'Aviso de branch: não medi o remoto (%s); as duas direções ficam sem resposta e o estado da fatia pode existir só neste branch.\n' "$1"
  exit 70
}
git remote get-url origin >/dev/null 2>&1 || nao_medi 'sem origin configurado'
LEITURA=$(git ls-remote --symref origin HEAD 2>/dev/null) || nao_medi 'a leitura de origin não respondeu'
PADRAO=$(printf '%s\n' "$LEITURA" | awk '$1=="ref:" && $3=="HEAD" {sub(/^refs\/heads\//,"",$2); print $2; exit}')
SHA=$(printf '%s\n' "$LEITURA" | awk '$1!="ref:" && $2=="HEAD" {print $1; exit}')
{ [ -n "$PADRAO" ] && [ -n "$SHA" ]; } || nao_medi 'a leitura de origin veio sem branch padrão ou sem sha'
ATUAL=$(git symbolic-ref --quiet --short HEAD 2>/dev/null) || ATUAL='(HEAD solto)'
[ "$ATUAL" != "$PADRAO" ] || exit 0    # no próprio padrão não há branch à frente a avisar
# `cat-file -e` SEM peel: o objeto ausente sai 1 e nunca fatal. Com peel sai 128,
# e 128 é "não consegui olhar" vestido de "não".
git cat-file -e "$SHA" >/dev/null 2>&1; NO_DISCO=$?
if [ "$NO_DISCO" -eq 1 ]; then
  printf 'Aviso de branch: %s, atrás de %s: sim, o commit publicado não está no meu disco; à frente: não medido, porque medi-lo exigiria buscar o objeto, e buscar escreve ref%s\n' \
    "$ATUAL" "$PADRAO" "$RESSALVA"
  exit 74
fi
[ "$NO_DISCO" -eq 0 ] || nao_medi 'a presença do publicado no disco não respondeu'
FRENTE=$(git rev-list --count "$SHA..HEAD" -- specs/ 2>/dev/null) || nao_medi 'a contagem local não respondeu'
ATRAS=$(git rev-list --count "HEAD..$SHA" -- specs/ 2>/dev/null) || nao_medi 'a contagem local não respondeu'
{ [ -n "$FRENTE" ] && [ -n "$ATRAS" ]; } || nao_medi 'a contagem local veio vazia'
[ "$FRENTE" -gt 0 ] || [ "$ATRAS" -gt 0 ] || exit 0    # nada a avisar
printf 'Aviso de branch: %s em specs/: à frente de %s em %s commit(s), atrás em %s commit(s). Medido agora no remoto por leitura, sem escrever ref%s\n' \
  "$ATUAL" "$PADRAO" "$FRENTE" "$ATRAS" "$RESSALVA"
exit 0
```
