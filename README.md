# itxpro-sdd

Framework de Spec-Driven Development da ITXPRO como plugin do Claude Code. A spec é a fonte da intenção, o código é consequência: cada fatia passa por mesas de Intenção, Desenho e Veredito, com portões humanos e veto que sobrevive ao consenso.

## Instalação

```
/plugin marketplace add conexaoarteiro/itxpro-sdd-plugin
/plugin install itxpro-sdd@itxpro-sdd-plugin
```

Instale sempre pinado em tag (`vX.Y.Z`), nunca em branch. O repositório de distribuição é público; a fonte do framework é o repositório canônico da ITXPRO.

## Pré-requisito: gitleaks

O gate de segredo em commit é fail-closed: sem gitleaks (>= 8.21.0) no PATH, commit nenhum passa. A instalação do gitleaks é sua, executada por você: o plugin imprime o comando e recomenda verificar o checksum do binário contra o release oficial. Nenhum agente executa esse download.

## Plugins recomendados

O framework adota skills de outros plugins como mecânica de execução dentro das mesas. A lista, com fonte oficial, comando de instalação e o que degrada sem cada um, vive na tabela "Plugins de terceiros: instalação" de `base/skills-padrao.md` (copiada para `docs/skills-padrao.md` do projeto na adoção). Fonte única: não existe segunda lista.

Nenhum deles é pré-requisito: sem o plugin o agente segue sem a skill, e a constituição continua regendo o processo. O setup confere a tabela contra o registro local de plugins instalados, lista o que falta com o comando e grava como pendência; ele nunca instala nada e nunca acessa a rede. Se o registro local não puder ser lido, o setup diz "não verificado" e trata a lista inteira como pendência, nunca como presente.

Além do gitleaks, o plugin usa `python3` (hooks nativos) e `gh` (backlog fora do contexto via GitHub Issues).

## O que o plugin disponibiliza

- Comando `/sdd`: o ponto de entrada único. Detecta o estado do projeto e despacha.
- Skill `sdd-setup`: entrevista em seis blocos (~15 minutos) que preenche a constituição do seu projeto e instancia o esqueleto. "Não sei" vale e vira pendência declarada.
- Skill `sdd-conductor`: o condutor do pipeline de fatias.
- Nove agentes: as vozes das mesas (spec-writer, architect, security-privacy-architect, ux-architect, devsecops, implementer, reviewer, grc-reviewer com veto, agent-experience-architect engatilhado).
- Hooks de enforcement: gate de segredo em commit, aviso de implementação sem spec aprovada, teto de 120 linhas da constituição, mais as regras hookify no payload de setup.
- Payload `base/`: constituição-template com lacunas, templates dos artefatos da fatia (01-spec, 03-plan, 04-tasks) e o seed do mapa do sistema em `templates/`, cartões de padrão de engenharia em `padroes/`, fluxo SDD, diagrama do pipeline e configuração do gitleaks.

## Depois de instalar

Rode `/sdd`. Sem constituição no projeto, ele aponta o setup; com constituição fechada, ele conduz a fatia.

## Paralelismo: versione a camada de enforcement

O condutor despacha em paralelo as tarefas que o plano declara independentes, cada uma no seu worktree. Antes de despachar, ele confere se o gate de segredo está vivo dentro daquele worktree: `.gitleaks.toml` na raiz de lá, o hook respondendo e uma prova de fail-closed com segredo sintético. Arquivo presente não basta.

Worktree novo nasce só com o que o git rastreia. Recomendação de adoção: comite a camada de enforcement no seu repositório e confira que o `.gitignore` não a exclui.

- `.gitleaks.toml` na raiz: o gate resolve a raiz daquele worktree e exige a configuração ali; sem ela, ele nega todo commit de lá.
- `.github/workflows/gitleaks.yml`: os ramos paralelos entram por um PR de integração. A varredura de CI é autoritativa onde a proteção de branch exige o check, e ali ela barra o merge; onde a proteção não exige, ela é sinal e o controle é a leitura humana do diff no PR.
- `.claude/` com as regras de aviso do setup: elas avisam no worktree onde o trabalho acontece, antes do commit.

Faltando qualquer peça, a conferência pega e o despacho cai para execução serial, sem perguntar. É o fail-closed funcionando, não defeito. Nada disso é pré-requisito de instalação: o plugin instala, o `/sdd` conduz e a fatia fecha do mesmo jeito, uma tarefa por vez. O que você perde é o paralelismo.

**Feche conflito por qualquer dos quatro caminhos (`git commit` ou `--continue`): o gate local varre o índice nos quatro. Código de ramo paralelo entra por PR, obrigatório; o CI é autoritativo onde a proteção de branch exige o check e sinal onde não exige.** Ficam fora do gate local `git revert --continue` e `git am --continue`, limite de escopo declarado (issue #62 do canônico). O resto do que fica fora segue uma regra só: o gate lê o comando como texto, em tokens separados por espaço em branco, e o shell monta um `argv` que essa leitura não enxerga. Onde o `argv` do git e a leitura do gate divergem, o gate cala, e ali só o CI alcança o segredo, já no PR e já gravado no ramo. A descrição dos quatro caminhos e das duas camadas está na seção "Integração dos ramos" de `skills/sdd-conductor/SKILL.md`.

## Voltar de versão

Rollback do adotante é roll-forward: uma tag nova, publicada pelo workflow de release, com o conteúdo desejado. Reinstale pinado nessa tag. Nunca edite o repositório de distribuição na mão: só o workflow escreve nele.

## Local-only

Nada sai da sua máquina. O plugin não tem telemetria, não faz chamada de rede em arquivo executável e as respostas da entrevista só vivem em arquivos do seu repositório.

## Feedback e melhorias

- **Onde**: issues públicas do repositório do plugin, https://github.com/conexaoarteiro/itxpro-sdd-plugin/issues. Não existe outro canal.
- **O que informar**: a versão instalada (`itxpro-sdd@X.Y.Z`, primeira linha de toda resposta do `/sdd`), a área (`sdd-conductor`, `sdd-setup`, `hooks` ou `payload`), o que você esperava e o que aconteceu, por categoria. A issue é pública: nunca cole segredo, log bruto, `.env`, conteúdo de constituição com dado de cliente nem dado pessoal.
- **O que esperar**: comentário de triagem do mantenedor e labels de estado (`triada`, `em-fatia`, `aguardando-release`); a issue fica aberta até a versão que a resolve e fecha citando essa versão, com o número da issue na entrada correspondente do `CHANGELOG.md`.
- **Se for lacuna do framework no seu projeto**: registre a decisão local em `docs/decisoes/` e abra a issue; a constituição gerada pelo setup traz essa regra.
