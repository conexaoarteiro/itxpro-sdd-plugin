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

## Voltar de versão

Rollback do adotante é roll-forward: uma tag nova, publicada pelo workflow de release, com o conteúdo desejado. Reinstale pinado nessa tag. Nunca edite o repositório de distribuição na mão: só o workflow escreve nele.

## Local-only

Nada sai da sua máquina. O plugin não tem telemetria, não faz chamada de rede em arquivo executável e as respostas da entrevista só vivem em arquivos do seu repositório.

## Feedback e melhorias

- **Onde**: issues públicas do repositório do plugin, https://github.com/conexaoarteiro/itxpro-sdd-plugin/issues. Não existe outro canal.
- **O que informar**: a versão instalada (`itxpro-sdd@X.Y.Z`, primeira linha de toda resposta do `/sdd`), a área (`sdd-conductor`, `sdd-setup`, `hooks` ou `payload`), o que você esperava e o que aconteceu, por categoria. A issue é pública: nunca cole segredo, log bruto, `.env`, conteúdo de constituição com dado de cliente nem dado pessoal.
- **O que esperar**: comentário de triagem do mantenedor e labels de estado (`triada`, `em-fatia`, `aguardando-release`); a issue fica aberta até a versão que a resolve e fecha citando essa versão, com o número da issue na entrada correspondente do `CHANGELOG.md`.
- **Se for lacuna do framework no seu projeto**: registre a decisão local em `docs/decisoes/` e abra a issue; a constituição gerada pelo setup traz essa regra.
