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

Nenhum deles é pré-requisito: sem o plugin o agente segue sem a skill, e a constituição continua regendo o processo. O setup confere a tabela contra o registro local de plugins instalados, lista o que falta com o comando e grava como pendência; essa conferência lê só o disco, nunca instala nada e nunca acessa a rede. Em outros passos o setup acessa a rede, e a seção "O que sai da sua máquina" nomeia cada chamada. Se o registro local não puder ser lido, o setup diz "não verificado" e trata a lista inteira como pendência, nunca como presente.

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

## O que sai da sua máquina

O plugin não tem telemetria: nada vai para a ITXPRO nem para servidor de terceiro. O que sai vai para o **seu** remoto e para o **seu** rastreador de issues, pela credencial que o `git` e o `gh` já têm configurada aí. O plugin nunca imprime, nunca guarda e nunca envia essa credencial. Onde a URL do seu `origin` carrega usuário e senha, o rito corta os dois do endereço antes de usá-lo, e o que sobra é só o host e o nome do repositório. O repositório alvo de toda chamada sai do `origin` deste checkout, com uma exceção que a lista de escrita nomeia.

O rito também **escreve** fora do seu disco, e essa escrita não estreia na 0.10.0: o `git push` do fechamento e o PR da leva já saíam, e as duas pendências do setup já viravam issue onde havia GitHub. Esta versão acrescenta escritas a essa conta e a enumera pela primeira vez. Por isso a lista vai completa, e ela vem com a régua que a sustenta: na hora de empacotar, um gate lê todo comando que o rito manda rodar e reprova o pacote se achar chamada de rede fora da lista revisada. A régua alcança o que o rito executa sozinho, e é dela que saem as duas listas abaixo. Ela não alcança passo que o condutor faz à mão com você. Existe um, ele é escrita, e ele aparece nomeado na lista, com o que a régua não garante nele.

**Leitura. Sai a pergunta, não o seu conteúdo.**

- `git ls-remote --symref origin`: o `/sdd` chama para avisar se o seu branch está à frente do publicado, e o condutor chama na abertura e no fechamento da fatia, para comparar o que você tem com o que está publicado. Sai a pergunta pelas refs. Nenhum arquivo seu viaja, e nenhuma ref sua é escrita, atualizada ou apagada.
- `gh api repos/<dono>/<repositório>/...`: o condutor chama para saber qual é o branch padrão, quais checks o branch exige, como terminaram os checks de um commit e se o rótulo da issue existe. Sai o nome do repositório, o nome do branch, o sha e o nome do rótulo.
- `gh run list`: o condutor chama enquanto espera os checks obrigatórios terminarem. Sai o nome do repositório e o sha.
- `gh label list`: o setup chama antes de criar rótulo, para não tocar no que já existe, e de novo antes de abrir issue, para conferir se o rótulo dela está lá. Sai o nome do repositório.

**Escrita. Sai texto, e onde sobe commit sai o que você comitou, imagem de evidência incluída. Tudo nasce no seu repositório e leva o seu nome na autoria.**

- **Os rótulos `P0`, `P1` e `P2`**, criados pelo setup uma vez, quando o projeto usa GitHub Issues como backlog. Carregam nome, cor e descrição fixos, iguais em todo projeto. Rótulo de mesmo nome que já exista fica intacto: o setup diz que encontrou e não toca.
- **A issue "Criar design system na primeira fatia com UI"**, criada pelo setup só quando você responde "não tenho" na camada de design system. Ela carrega uma resposta da sua entrevista: que o projeto não declarou design system.
- **A issue "Ativar required check do gitleaks quando o plano permitir"**, criada pelo setup só quando a pergunta do required check fecha em "sim", "não sei" ou sem resposta. Ela carrega que o gitleaks ainda não é check obrigatório no branch padrão deste repositório.
- **A issue de ressalva do Veredito**, o ponto que a mesa final anotou e que não virou tarefa. O condutor só a cria com a palavra de autorização dada naquela execução, nunca sem ela. Ela carrega título curto e link para o registro da mesa, que fica no seu repositório; o texto da ressalva não vai no corpo.
- **O `git push origin HEAD:<branch padrão>`** do fechamento que você aprova. Sobem os commits da fatia, código e artefatos, como em qualquer push seu.
- **O PR**, em dois momentos. Quando a fatia roda tarefas em paralelo, o condutor junta os ramos prontos num ramo de integração e abre um PR único da leva, que é o caminho obrigatório desse código; no fechamento, ele só abre PR se você pedir e o `gh` estiver instalado. Sai o que um PR precisa para existir: os commits daqueles ramos, código e artefatos, no seu remoto, mais o título e o corpo que o condutor escreve, que dizem o motivo em prosa e nunca URL de remoto, token, caminho absoluto, conteúdo de arquivo ou saída bruta do `git`. **Este passo o condutor executa à mão, e ele é o único da lista fora da régua:** o gate do empacote não o alcança, porque ele não está escrito como comando do rito, e a amarra do `origin` que vale para as chamadas acima não passa por ele. Quem responde por ele é você, dentro da execução que você conduz.

As respostas da entrevista vivem em arquivos do seu repositório, com as duas exceções nomeadas acima. Se o seu repositório for público, o rastreador dele é público junto, e o que essas issues carregam fica visível. Nenhuma escrita reescreve nem apaga issue, rótulo, ref ou branch que já existe. O push do fechamento toca um ref que existe, o do seu branch padrão, e só o avança para a frente, sem `--force`. Nenhuma delas baixa ou instala binário.

Duas chamadas acontecem fora da sua máquina, e vão nomeadas junto. As duas saem do workflow `gitleaks.yml` do payload, depois que você o comita, e as duas rodam no seu CI: o runner busca a action `actions/checkout`, pinada por sha completo, e o job baixa o gitleaks a cada varredura, em versão pinada e com checksum SHA256 conferido antes de executar.

## Feedback e melhorias

- **Onde**: issues públicas do repositório do plugin, https://github.com/conexaoarteiro/itxpro-sdd-plugin/issues. Não existe outro canal.
- **O que informar**: a versão instalada (`itxpro-sdd@X.Y.Z`, primeira linha de toda resposta do `/sdd`), a área (`sdd-conductor`, `sdd-setup`, `hooks` ou `payload`), o que você esperava e o que aconteceu, por categoria. A issue é pública: nunca cole segredo, log bruto, `.env`, conteúdo de constituição com dado de cliente nem dado pessoal.
- **O que esperar**: comentário de triagem do mantenedor e labels de estado (`triada`, `em-fatia`, `aguardando-release`); a issue fica aberta até a versão que a resolve e fecha citando essa versão, com o número da issue na entrada correspondente do `CHANGELOG.md`.
- **Se for lacuna do framework no seu projeto**: registre a decisão local em `docs/decisoes/` e abra a issue; a constituição gerada pelo setup traz essa regra.
