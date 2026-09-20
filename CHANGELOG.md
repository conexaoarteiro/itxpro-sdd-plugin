# Changelog — itxpro-sdd

Régua de versão, pela ótica do contrato que o agente adotante lê: major quebra nome, caminho ou instrução existente; minor adiciona sem quebrar; patch corrige texto.

O hash autoritativo de cada versão é o `INTEGRIDADE.txt` da tag correspondente no repositório de distribuição; a linha `Integridade:` aqui é cópia gravada após o release.

## 0.10.0 — 2026-09-19

Classificação: minor, como na 0.9.0: muda comportamento sem que nome, caminho ou instrução deixe de resolver. A régua de major ganha dois gatilhos: arquivo distribuído que muda de caminho ou de nome; contrato prescrito que muda de significado, seja verbo que passa a responder outra pergunta, código de saída que troca de causa ou passo removido do rito.

A classificação foi medida, e a medida vai aqui em vez da afirmação. O primeiro gatilho não dispara: o pacote carrega os mesmos arquivos da 0.9.0, um a um, nenhuma linha de cópia do empacote mudou de destino e nada foi renomeado, movido ou removido. O segundo disparava, e esta versão o desarmou antes de publicar. O código `13` do Passo 5 significava, até a 0.9.0, o branch padrão que a resolução LOCAL não achava; essa resolução saiu do passo porque escrevia ref no repositório de quem só queria uma resposta, e o número tinha sido reaproveitado para a causa nova, o remoto que responde sem o par nome e sha. Causa diferente no mesmo número é o segundo gatilho na letra. O reaproveitamento foi desfeito: o `13` está aposentado, nada o emite, e a condição nova nasce no `18`, em faixa livre. Varrido o resto da faixa do Passo 5, `10`, `11`, `14`, `15` e `16` respondem pela mesma causa da 0.9.0, com o `15` aceitando um caminho a mais e recusando o mesmo resto; o `12` trocou a primitiva, de busca para leitura do remoto, e continua dizendo a mesma coisa, o remoto não respondeu; e o `17` é novo, em faixa livre, para separar "não medi a ancestralidade" de "não é ancestral", distinção que a 0.9.0 não tinha porque a busca punha o objeto no disco antes da medida. Na conferência do despacho, o `51` continua significando o que significava, e as outras três causas que ele cobria saíram para `52`, `53` e `54`. Com o `13` aposentado, nenhum dos dois gatilhos dispara.

Adiciona:

- Passo 0 de retomada, que mede sem escrever ref: sincronia, ramo, sessao, boxes e varre; no fechamento, checks, ressalvas e abre.
- `sdd-setup`: roadmap com coluna Estado, rótulos P0, P1 e P2 sem tocar label existente, e issue nasce rotulada.
- Duas regras normativas novas em `base/fluxo-sdd.md`, as duas piso para os agentes de quem adota e as duas com escopo nominal e fechado. A redação normativa delas mora lá, casa única, e este anúncio a resume sem copiá-la. **A regra da materialização** cobra passo prescrito para o estado que tem de durar além da fatia, e passo prescrito ali são três coisas juntas: escritor nomeado, destino em disco que a sessão seguinte abre e o commit em que a escrita acontece. O escopo são quatro casos: tarefa de duas metades cuja segunda metade acontece depois do merge; ressalva do Veredito que não vira tarefa da fatia; linha da fatia no roadmap, no fechamento de fase; e box de critério cumprido fora do repositório. **A regra da medida nomeada** cobra que o rito diga qual pergunta mediu e recusa resposta mais larga que a medida; a segunda metade dela trata a medição que não separa dois estados, e manda devolver os dois nomeados em vez de escolher o mais confortável. O escopo são seis casos, entre eles a sincronia entre o disco e o remoto, a abertura de sessão que lê só o git local, o código de dúvida que cobre dois motivos e o sinal externo que o passo espera e não encontra. Nas duas, caso novo entra por decisão que o nomeie, nunca por semelhança com os casos listados. A skill do condutor e o mandato do reviewer citam as duas pelo nome e pelo caminho.
- Três variáveis de ambiente opcionais na skill do condutor, todas com default no próprio fence e nenhuma obrigatória. `SDD_TETO_ESPERA` e `SDD_INTERVALO_ESPERA` mudam o teto e o intervalo da espera dos checks, com 300 s e 10 s de default, e nascem travadas: elas encurtam a espera e nunca a alongam, com teto acima do default caindo no default e intervalo abaixo do piso caindo no piso. `SDD_FERRAMENTA_SESSAO` é de outra natureza e vale ler com atenção: com o valor `disponivel` ela declara que o host expõe a ferramenta de renomear a sessão, e qualquer outro valor, a variável vazia e a variável ausente valem todos como ausência, que é o default e o ramo seguro. Ela é fronteira de confiança declarada, o único ponto do Passo 0 em que o verbo acredita em quem o chamou, e existe porque não há arquivo, ref nem chamada de git que responda se esta sessão pode ser renomeada. Nenhum dos dois ramos renomeia coisa alguma: o verbo imprime o título e diz qual ramo seguiu.
- Escrita nova no seu remoto e no seu rastreador, nomeada aqui porque parte do que esta versão acrescenta não fica no seu disco. O `sdd-setup` cria os três rótulos, ato que a 0.9.0 não tinha, e as duas issues de pendência dele saem da prosa e viram chamada do `gh`. No fechamento, o verbo `abre` cria a issue da ressalva do Veredito, e só com a palavra de autorização daquela execução. Escrita fora do seu disco não estreia nesta versão: na 0.9.0 as duas pendências já viravam issue onde havia GitHub, por prosa em vez de chamada, e o `git push` do fechamento e o PR da leva já saíam. Quem enumera a conta inteira, leitura e escrita, com a régua que a sustenta e o passo que ela não alcança, é a seção "O que sai da sua máquina" do `README.md` do pacote, casa única; este anúncio não a copia.

Muda comportamento: o Passo 5 perdeu `git fetch` e `git remote set-head`, lê com `git ls-remote --symref` e não avança mais o ref local do branch padrão. Atualize-o se dependia dele. Junto com a busca saiu o código de saída `13`: quem casava `13` para mandar recompor a ref local do branch padrão cai agora no ramo do código desconhecido, que é parar e perguntar, e nunca numa instrução que deixou de valer. No fence da conferência do despacho, o verbo `volta` passa a falhar fechado quando a leitura do que o ramo tocou não acontece: o caso que saía `0`, "sem desvio", com `git diff` ou `git ls-files` falhando, agora sai `53`, "não medi", que é código novo desta versão. Quem lê `0` como liberação recebe uma liberação falsa a menos; quem não conhece o `53` cai no mesmo ramo do código desconhecido.

Migração (nota da 0.10.0):
1. O `sdd-setup` copia só o que não existe (copy-if-absent) e nunca sobrescreve arquivo que já está no projeto. Quem rodou o setup na 0.9.0 ou antes tem um `docs/fluxo-sdd.md` sem as duas regras normativas novas, e atualizar o plugin não o altera: o arquivo já existe, então a cópia não acontece e o setup reporta e segue.
2. Leve você mesmo. Compare antes de copiar, na sessão com o plugin carregado: `diff "${CLAUDE_PLUGIN_ROOT}/base/fluxo-sdd.md" docs/fluxo-sdd.md`. Se você não customizou o fluxo, copie o arquivo inteiro. Se customizou, traga só as duas seções novas, a **regra da materialização** e a **regra da medida nomeada**, em vez de sobrescrever: a cópia cega apaga a sua customização.
3. Sem elas, a citação não resolve no seu projeto. A skill do condutor e o mandato do reviewer citam as duas pelo nome e pelo caminho, e o caminho que eles citam é o seu `docs/fluxo-sdd.md`. Quem não copiar fica com agentes que apontam para regra que o projeto não tem, e o piso que esta versão acrescenta não vale ali.
4. O mesmo vale, mais fraco, para os três rótulos. O setup cria `P0`, `P1` e `P2` uma vez, no esqueleto, e não toca em label que já existe. Quem rodou o setup antes desta versão não os tem: crie os três à mão no seu rastreador, com a cor que preferir. Rodar o setup de novo também os cria, e nesse caminho conte com a segunda cópia das duas issues de pendência dele, que é limite conhecido desta versão.
5. Nada aqui é obrigatório para o plugin continuar rodando. Nenhum nome ou caminho mudou, e projeto que não copiar segue funcionando no comportamento da 0.9.0 para estes dois pontos, com a diferença declarada acima.

Integridade: sha256:0e785bf6cce8907bfa853dd3180680432efcab28736d8a0c44e168a9621126eb (amarração 0.10.0 → hash; conjunto do pacote, excluindo CHANGELOG.md e INTEGRIDADE.txt).

## 0.9.0 — 2026-09-16

Classificação: minor (muda o que um script distribuído grava, onde grava e o que diz; precedente da 0.8.0, em que o comportamento de enforcement mudou sem nome, caminho ou instrução deixar de resolver; nenhum agente lê o log como contrato; quem tem o arquivo antigo precisa ler esta entrada, e patch a subcomunicaria).

Corrige:

- O hook `spec-approval-warn` deixa de gravar caminho absoluto (plugin#13). O log passa a morar em `$(git rev-parse --git-common-dir)/itxpro-sdd/hooks-log.jsonl`, fora da árvore de trabalho e nunca indexado. O campo `path` de cada linha passa a ser um destes três: o caminho relativo à raiz do projeto, o marcador `fora-da-raiz` ou `erro-interno: <tipo>`. Sem diretório git resolvível, o hook não grava nada. O texto da mensagem do hook mudou: ele diz onde o log mora e o que a linha carrega.

Quem adotou o plugin em qualquer versão de 0.1.0 a 0.8.0 tem `.claude/hooks-log.jsonl` na raiz do projeto, com caminhos absolutos que carregam o nome de usuário do sistema. O hook novo nunca lê nem reescreve o log antigo; nem o hook nem o setup agem sobre ele. O roteiro abaixo é do adotante.

Migração (nota da 0.9.0):
1. Confira índice e histórico: `git ls-files --error-unmatch .claude/hooks-log.jsonl` diz se o arquivo está no índice; `git log --all --oneline -- .claude/hooks-log.jsonl` lista os commits que o carregam.
2. Se está no índice: `git rm --cached .claude/hooks-log.jsonl`, linha `.claude/hooks-log.jsonl` no `.gitignore` e commit.
3. Apague o arquivo antigo: `rm -f .claude/hooks-log.jsonl`. As linhas velhas carregam o caminho absoluto, e a métrica do log perde essas linhas; a perda é aceita.
4. Se o histórico carrega o arquivo e o remoto é compartilhado ou público, o dado já saiu da máquina. Decida: reescrever o histórico com `git filter-repo --invert-paths --path .claude/hooks-log.jsonl` (ou `filter-branch`), depois `git reflog expire --expire=now --all && git gc --prune=now` e `git push --force`, que a proteção de branch pode barrar e que obriga todo clone a re-clonar; ou conviver com a exposição. A reescrita não apaga o que já foi clonado, bifurcado ou guardado pelo provedor: em fork e em ref de pull request os objetos continuam, e commit reescrito segue acessível por SHA até o host purgar; remoção completa exige pedido ao suporte do host. O plugin não reescreve histórico.

Integridade: sha256:c028bbe707a23680d03e98960427d9c5a3647333e6611e78843c25bc59943ca3 (amarração 0.9.0 → hash; autoritativo no `INTEGRIDADE.txt` da tag v0.9.0)

## 0.8.0 — 2026-09-04

Classificação: minor (adiciona cobertura ao gate local e à varredura do CI; muda comportamento de enforcement e pode pintar de vermelho check que era verde; nenhum nome, caminho ou instrução deixa de resolver).

Adiciona:

- Gate local de segredo nos três `--continue` (#56 do canônico): `git merge --continue`, `git rebase --continue` e `git cherry-pick --continue` passam pela mesma varredura do índice que o `git commit` já tinha, com o mesmo fail-closed e a mesma negação, regra citada e valor mascarado. Opções entre o verbo e o `--continue` são toleradas (`git cherry-pick --no-edit --continue` cai no gate); `--abort`, `--skip` e `--quit` não o disparam. O gate casa também a abreviação que o git aceita: `git merge --cont` e `git rebase --cont` são a mesma opção `--continue` e caem nele, `--co` e `--c` o git recusa como ambíguas, e no `cherry-pick`, onde o git recusa toda abreviação, o gate varre mesmo assim.
- Dois passos de varredura no workflow `gitleaks.yml` (#57 do canônico), no mesmo job e com o nome do check inalterado. O passo de histórico roda com `--log-opts="--full-history --all --diff-filter=tuxdb -m"`: a opção substitui o comando default do binário em vez de acrescentar a ele, por isso o valor repete o default inteiro e soma o `-m`, que faz o merge commit ser lido contra cada pai. O passo de árvore roda `gitleaks dir .` sobre o resultado do checkout e enxerga o conteúdo que nasce na resolução de conflito, invisível ao patch. Os dois passos usam `--redact`, e nenhum tem `continue-on-error`.
- Cartão de padrão `gitleaks` na v1.1, com a cobertura dos dois passos e o que fica fora dela.
- Instrução dos quatro caminhos liberados, na redação aceita na spec: "Feche conflito por qualquer dos quatro caminhos (`git commit` ou `--continue`): o gate local varre o índice nos quatro. Código de ramo paralelo entra por PR, obrigatório; o CI é autoritativo onde a proteção de branch exige o check e sinal onde não exige."

Corrige:

- Texto que declarava o buraco aberto nas casas que viajam. O README do plugin e a skill `sdd-conductor` diziam que o gate local casava só `git commit`, que a varredura do CI não enxergava o que nascia numa resolução de conflito e que o caminho era fechar conflito com `git commit`, nunca com `--continue`. O cartão `gitleaks` dizia outra coisa: na v1.0 ele descrevia o hook local como bloqueio de `git commit`, não citava os `--continue` e resumia o CI como o workflow que varre o repositório, sem separar histórico de árvore. Essa linha genérica prometia alcance que a varredura não tinha. As três casas passam a descrever o estado fechado, com a redação acima.
- Gate local que podia ficar preso antes de varrer (0.7.0 e anteriores). O reconhecimento do comando custava tempo demais em parte dos casos, e o Claude Code descarta o hook que estoura o timeout do host, sem bloquear a ferramenta: ali o commit nascia sem varredura nenhuma. O reconhecimento desta versão decide em fração de milissegundo e em tempo linear no tamanho do comando, e os timeouts internos do gate seguem fechando antes do timeout do host. Quem está na 0.7.0 atualiza por isso, e não só pela cobertura nova.

Migração (nota da 0.8.0):
1. Check `gitleaks` que era verde pode ficar vermelho onde há segredo em merge commit. Segredo que já estava no histórico: remova e rotacione. Falso positivo: allowlist de path exato no `.gitleaks.toml`, via PR.
2. Fingerprint de `.gitleaksignore` gravado no modo histórico não vale no modo de árvore: o `gitleaks dir` usa `arquivo:regra:linha`, sem commit.
3. Achado antigo silenciado por fingerprint de commit ganha fingerprint novo com a leitura do merge commit, e o silêncio antigo deixa de cobri-lo.
4. Com o `-m`, achado em merge commit aparece uma vez por pai, com o mesmo fingerprint: duas linhas são um segredo, não dois.
5. Migre o silêncio para path exato no `.gitleaks.toml`, via PR; nunca diretório inteiro nem regex.
6. O `sdd-setup` copia só o que não existe (copy-if-absent) e nunca sobrescreve arquivo que já está no projeto: leve você mesmo o `base/gitleaks.yml` da v0.8.0 para o seu `.github/workflows/gitleaks.yml`. Compare os dois antes de copiar, na sessão com o plugin carregado: `diff "${CLAUDE_PLUGIN_ROOT}/base/gitleaks.yml" .github/workflows/gitleaks.yml`. Se você mudou o gatilho (`on:`), o runner (`runs-on:`), o nome do job (`name:`) ou acrescentou passos, a cópia cega apaga a sua customização, e aí traga só os dois passos de varredura para o seu arquivo em vez de sobrescrever. O nome do job é o nome do check: a cópia cega renomeia o check, a proteção de branch fica exigindo um nome que ninguém mais reporta e a fila de PR trava.
7. Quem ainda não copiou o `gitleaks.yml` da v0.8.0 está no estado da 0.7.0, com a cegueira declarada no CHANGELOG 0.7.0; copiar é o único caminho que fecha.

Integridade: sha256:e7e882c8d4e8e3b0725fc5c5decf7198a9913c89744a59016076e83e47366a03 (amarração 0.8.0 → hash; autoritativo no `INTEGRIDADE.txt` da tag v0.8.0)

## 0.7.0 — 2026-08-21

Classificação: minor (adiciona perfil de tarefa, superfície declarada, despacho paralelo e estado de execução; com a regra de migração abaixo, nenhum plano escrito antes desta versão deixa de resolver e nenhum nome ou caminho muda).

Adiciona:

- Perfil de tarefa em vocabulário fechado (#40 do canônico): `texto | front | back | infra`, sempre o primeiro token do sufixo da tarefa. Perfil não tem default e não se infere: tarefa sem perfil, ou com palavra fora do vocabulário, bloqueia o despacho dela mesma, nomeada, e as demais seguem. O perfil roteia a carga de insumo do implementer e é aditivo: acrescenta skills e itens de pronto, nunca dispensa item do piso nem substitui o checklist de pronto, que mora em `agents/implementer.md`, casa única. O perfil `dados` fica engatilhado, com um evento de acordar só e observável no plano: a primeira fatia que cria tabela, altera esquema ou move dado em lote, e essa fatia refaz a triagem de segurança do zero.
- Superfície declarada por tarefa, no campo `toca:` do mesmo sufixo. É ela que torna a independência falseável por ferramenta em vez de confiável por palavra: antes do despacho o condutor expande os caminhos declarados e cruza os conjuntos par a par; na volta, confere o que o ramo tocou contra o que a tarefa declarou e nomeia o desvio. Serial é o default, e omissão, prosa no lugar de caminho, dúvida ou superfície que cruza significa uma tarefa de cada vez. Com isso a marcação `independente`, que nasceu declarativa e dormente na 0.6.0, passa a executar; quem paraleliza é o condutor, e o implementer nunca dispara execução por conta.
- Interlock de enforcement pela matéria tocada, nunca pelo rótulo do perfil: declaração `toca:` que alcance `.gitleaks.toml`, `.github/workflows/`, `.claude/settings.json`, `hooks.json`, `.claude/hooks/` ou `hooks/` na raiz do repositório serializa sozinha, em qualquer perfil, e nunca recebe `independente`. O registro do hook entra por nome próprio, porque é ele que liga o gate ao commit: dois ramos reescrevendo o registro ao mesmo tempo deixam sem resposta qual gate valeu em qual commit. O diretório de hooks entra ancorado, e a âncora existe para não prender hook de front-end: `src/hooks/` e `app/hooks/` não são caminho de enforcement e não serializam. Fora da raiz e de `.claude/`, um diretório de hooks só conta quando ele carrega o registro, o arquivo de versão ou os scripts do gate; a prova é o vizinho em disco, nunca o nome do diretório acima. Esses arquivos formam um conjunto único; serem arquivos diferentes não os torna superfícies disjuntas. O piso ganha a mesma âncora em `base/fluxo-sdd.md`: piso não paraleliza, controle e artefato nunca caem em ramos distintos (a política nasce no ramo da tabela, o header de segurança nasce no ramo da página pública) e colisão entre piso e paralelismo é estouro, sobe ao dono.
- Triagem de despacho na skill do condutor: tabela de decisão aplicada tarefa a tarefa, que para na primeira linha que casa, com a mensagem literal do bloqueio por perfil ausente e o teto de três execuções simultâneas. O teto mede raio de explosão, não gasto de token, e a constituição do projeto o recalibra com registro no plano.
- Conferência do despacho como bloco executável sob cabeçalho fixo na skill do condutor, com quatro verbos (`triagem`, `cruza`, `gate`, `volta`) e códigos de saída em casa única. Texto e ferramenta não divergem em silêncio: a suíte extrai o bloco e o executa. O condutor traduz o código em uma linha de prosa, sem caminho absoluto e sem saída bruta de git.
- Worktree do despacho ancorado fora da árvore de trabalho indexada, sob o diretório comum do git, com um ramo por instância e nome derivável nos dois sentidos. Raiz fora da âncora não recebe tarefa, e o verbo `gate` mede a posição e devolve código próprio, porque worktree aninhado entra no índice como gitlink e repõe segredo plantado sob caminho que a allowlist ancorada não casa. Cobertura do gate de segredo se prova por ambiente e nunca se herda: configuração na raiz daquele worktree, hook presente e registrado, raiz que o gate resolve igual à do worktree, e sonda que discrimina, negando um segredo sintético e deixando passar conteúdo limpo. Gate cego também serializa, e a sonda nasce e morre em diretório temporário.
- Estado durável com escritor único: o condutor escreve o arquivo de tarefas da fatia, no checkout dele, e nenhum implementer marca box, nem no worktree dele. O box passa a carregar quatro estados no lugar de dois (`[ ]` não começou, `[~]` em execução, `[x]` fechada, `[!]` falhou), marcados no momento em que a mudança acontece, com o rastro de ramo e SHA curto no último campo do sufixo, sem linha nem campo novo na tarefa.
- Falha parcial que não contamina: ramo que falha marca só a própria tarefa, com o ramo e o commit em que parou, e as demais da leva seguem o próprio caminho. Ramo falhado não entra na integração, e o condutor descarta o worktree e o ramo, sem revert e sem histórico sujo. A retomada é só da tarefa que falhou, da mesma base, com a evidência da falha no mandato; segunda falha consecutiva no mesmo id para aquele despacho e sobe ao dono.
- Integração dos ramos por PR único: o condutor abre o ramo de integração, traz cada ramo pronto com `git merge --no-ff` e abre um PR só da leva. A divisão das camadas fica declarada, sem promessa a mais. O gate local de segredo casa o verbo `git commit` e varre o índice: conflito fechado com `git commit` cai nele e é negado com a regra citada e o valor mascarado, enquanto `git merge --continue`, `git rebase --continue` e `git cherry-pick --continue` não o disparam. A varredura de histórico do CI lê o patch de cada commit e é cega ao conteúdo que nasce na resolução, porque merge commit não tem patch próprio. Por isso o condutor fecha conflito com `git commit`, nunca com `--continue`. O CI do PR é autoritativo onde o check está exigido por proteção de branch; onde a proteção não existe, o CI reporta e o controle é a leitura humana do diff no PR. O fast-forward do fechamento segue valendo só para o artefato de fatia que ele já lista; código de ramo paralelo entra por PR, sempre.
- Degradação honesta do paralelismo em `base/skills-padrao.md`: o despacho paralelo roda em `git worktree` nativo e não cai sem plugin de marketplace; quem derruba a janela para serial é o gate não provado no worktree. O README ganha a seção de adoção correspondente: worktree novo nasce só com o que o git rastreia, então versione a camada de enforcement e confira que o `.gitignore` não a exclui. Faltando peça, a conferência pega e o despacho cai para serial sem perguntar, e a fatia fecha do mesmo jeito, uma tarefa por vez.

Corrige:

- Recomendação de retomada que morria em worktree novo (#53 do canônico): as duas casas do fechamento passam a perguntar "meu HEAD contém o publicado?" com `git fetch -q origin` e `git merge-base --is-ancestor origin/<padrão> HEAD`, e só a resposta falsa pede `git pull --ff-only origin <padrão>`, com remoto e ref nomeados. O teste não depende de upstream nem do nome do branch local; `pull` sem argumento morria antes do merge no ramo recém-aberto.
- Convenções de código da constituição-template sem viés de stack (#41 do canônico): o nome no código segue a convenção idiomática da linguagem declarada na stack, e o projeto declara qual vale quando há mais de uma, no lugar da regra de PascalCase de React afirmada como fato.

Migração (nota da 0.7.0): plano escrito antes desta versão continua rodando. A detecção é do arquivo de tarefas inteiro e é binária: zero token de perfil em todas as tarefas significa plano legado, e o condutor avisa uma vez, roda serial e segue, sem bloquear tarefa nenhuma. Um token que seja põe o arquivo sob a regra nova, e ali a tarefa sem perfil bloqueia a si mesma, nomeada, enquanto as demais seguem; tarefa `[DONO]` não entra nessa conta. Nenhum arquivo de tarefas escrito sob 0.6.x deixa de resolver e nenhum nome ou caminho muda: sobra adição. O modo legado é shim declarado e morre na 1.0.0, reservada para uma declaração de estabilidade do framework que esta versão não faz.

Integridade: sha256:61beba86019649aed996f99eccb823f6b823b7e39319a6e2d1287849175189d2 (amarração 0.7.0 → hash; autoritativo no `INTEGRIDADE.txt` da tag v0.7.0)

## 0.6.1 — 2026-08-21

Classificação: patch (corrige texto ilustrativo; nenhum nome, caminho ou instrução muda).

Corrige:

- Diagrama do pipeline (`base/diagrama-pipeline-sdd.svg`) alinhado à 0.6.0: a legenda do portão de Desenho nomeia os três gatilhos (divergência, veto, estouro de teto), a construção diz "cada implementer · uma tarefa por vez" e o carimbo de versão sai de 0.2.1. O normativo textual já saiu correto na 0.6.0; o diagrama tinha ficado fora do mapeamento da fatia 008.

Integridade: sha256:49f5c431fafe4a1625a4d929af0a91fd3922f34593416e630c98cb2d5051ad07 (amarração 0.6.1 → hash; autoritativo no `INTEGRIDADE.txt` da tag v0.6.1)

## 0.6.0 — 2026-08-20

Classificação: minor (adiciona triagem, teto, gatilho, cartões e mandatos; nenhum nome ou caminho que resolvia deixa de resolver).

Adiciona:

- Quarta triagem de proporcionalidade (#39 do canônico): tamanho da entrega vira classe de fatia (leve, média ou plena), assinada pela voz de segurança no registro de Intenção (`Classe: X, assinada por security`); registro sem a linha bloqueia a convocação do Desenho. Tetos de tarefas por classe: leve até 10, média até 20, plena sem teto fixo com justificativa; default do framework, recalibrável pela constituição do projeto com registro. Invariante de granularidade: um critério de pronto por tarefa, tarefa composta conta por critérios, fundir para caber é estouro disfarçado.
- Piso por classe em casa única na triagem de `base/fluxo-sdd.md`: o teto corta cerimônia, nunca piso; colisão entre piso e teto é estouro e sobe ao dono; página pública nunca dispensa headers e CSP herdados; templates e agentes apontam, não copiam.
- Portão de Desenho com três gatilhos nomeados (divergência, veto, estouro de teto; reclassificação para cima conta como estouro) e mensagem de estouro em formato fixo de até cinco linhas, com modelo literal na skill do condutor, sem anexar o plano; tarefa `[DONO]` com quatro campos, fora do caminho crítico, listada em "Tarefas suas".
- Pré-autorização condicional do portão de Intenção (#42 do canônico): frase-modelo literal em casa única no Passo 4 da skill; o Passo 5 dispara no fechamento do Desenho por exceção só com `Pré-autorização: emitida` no registro de Intenção e mesa fechada sem divergência, sem veto e sem estouro; regra de morte (anulada não renasce; Desenho escalado só publica com frase nova do dono); rastro triplo em campos fixos; a sequência de fechamento existente não mudou um byte.
- Fundação repetível em cinco cartões de padrão (`base/padroes/`): `ci-base.md`, `headers-csp.md`, `lighthouse-pa11y.md`, `deploy.md` e `gitleaks.md`, uma página cada, com versão, data de revisão e seção "Como verificar herança"; o plano declara só o delta e o gate de release verifica o formato de todo cartão distribuído; os três cartões anteriores ganham a mesma linha de versão.
- Texto canônico único do gatilho de superfície rica (#43 do canônico): o normativo vive na triagem de `base/fluxo-sdd.md`; skill do condutor e template de spec viram paráfrase marcada com apontador; a suíte do framework passa a acusar duplicata.
- Mandato de Veredito em UI simples (#44 do canônico): o ux-architect confere dois itens e para (barra visual com elemento construído nomeado; componentes contra o DS com desvio nomeado por arquivo), nunca julga fluidez nem exige moodboard em UI simples; o reviewer exige a citação nominal no veredito.
- "Uma tarefa por vez" passa a valer por implementer, não por fatia; o template de tarefas ganha marcadores em sufixo (núcleo, sustentação com motivo, `[DONO]`, `depende de:`/`independente`) e a marcação de independência é declarativa e dormente; o template de plano ganha a seção "Classe e orçamento de tarefas".

Migração (nota da 0.6.0): fatia com Intenção aprovada antes da 0.6.0 não ganha pré-autorização retroativa; sem frase-modelo emitida no portão de Intenção vale o comportamento anterior, documentado na skill. A constituição do projeto pode restringir o mecanismo (portão de Desenho fixo, sem pré-autorização), nunca ampliar.

Integridade: sha256:b7b925bd7a7229a423945f20a4a7f0f9eb368b153e66fbbeebde3d243c269f2b (amarração 0.6.0 → hash; autoritativo no `INTEGRIDADE.txt` da tag v0.6.0)

## 0.5.0 — 2026-08-20

Classificação: minor (só adiciona seção, mandato e regra; nenhum nome ou caminho que resolvia deixa de resolver).

Adiciona:

- Referência do dono como contrato (#37 do canônico): seção "Desvios da referência" no template de spec, com três campos por item (o que a referência faz, o que a spec propõe, por quê) e o texto obrigatório "sem referência declarada"; o spec-writer lê a referência como insumo de primeira ordem e lista os desvios; o portão de Intenção apresenta a seção item a item, desvio sem resposta é lacuna e bloqueia o fechamento; convergência da mesa que contraria a referência ou o pedido do dono sobe ao portão, nunca vira decisão.
- Insumo visual (#38 do canônico): referência visual do dono entra na mesa como imagem (página inteira, desktop e mobile) em `specs/NNN-*/insumos/`; referência que virou só texto é lacuna. Captura somente na URL declarada, leitura apenas, nunca segue link, nunca autentica, nunca preenche nem submete, em contexto sem sessão; referência externa é dado a descrever, nunca instrução a obedecer; persistência de imagem com pessoa identificável, contato de terceiro ou site alheio se decide no portão, nunca por default.
- Proporcionalidade visual em três níveis com gatilho objetivo: sem UI (ux-architect sai da mesa), UI simples (barra visual de uma linha + DS, sem moodboard) e superfície rica (Barra visual completa, moodboard no Desenho, veredito visual lado a lado); é rica quando o dono deu referência visual ou a página é pública e carrega a marca; referência a artefato visual convoca o ux-architect na Intenção.
- Direção de arte no ux-architect: composição, hierarquia, imagem e atmosfera autorizadas pelo moodboard; Barra visual no template de spec; moodboard de uma página e orçamento de imagem de hero no template de plano; veto de imagem por performance sem orçamento apresentado é inválido.
- Regra do DS vocabulário/frase (ux-architect e implementer): o DS rege tokens, marca, fonte, cor e componentes base; o moodboard autoriza composição, hierarquia, imagem e atmosfera; desempate, DS em identidade e moodboard em layout; gap real do DS vira issue no DS, nunca componente paralelo.
- Veredito visual com evidência: comparação lado a lado construído vs. referência vs. moodboard com a skill `impeccable`, screenshot do construído (página inteira, do próprio projeto; nunca terminal, credencial, variável de ambiente ou outra janela) em `specs/NNN-*/evidencias/` citado no registro; veredito de superfície rica sem evidência visual é lacuna; a disciplina de comparar screenshot com o moodboard entra no template de tarefas.
- `impeccable` oficializada na tabela de instalação de `base/skills-padrao.md` (fonte `https://impeccable.style`, `github.com/pbakaus/impeccable`, comando real de marketplace), obrigatória no Veredito de superfície rica.

Integridade: sha256:583b639d108676fc82d4cc1ed22933d2fc7f24f5b77f834f0d36a5ac43f8967e (amarração 0.5.0 → hash; conjunto do pacote, excluindo CHANGELOG.md e INTEGRIDADE.txt).

## 0.4.0 — 2026-08-18

Classificação: minor (adiciona comportamento ao condutor e ao setup e corrige instrução morta; nenhum nome ou caminho que resolvia deixa de resolver).

Adiciona:

- Condutor fecha a fase antes de recomendar sessão nova (plugin#1): com a aprovação do portão que anuncia o efeito, integra o branch de trabalho no branch padrão por fast-forward e publica em `origin`, só quando o diff se restringe a `specs/` e `docs/decisoes/`; nunca `--force`, `--no-verify` nem outro remoto; parada devolve à pessoa. "Estado em disco" passa a significar branch padrão publicado.
- `/sdd` avisa em uma linha quando o branch corrente está à frente do remoto em `specs/` e aponta o canal de feedback.
- Canal de feedback (plugin#2): seção "Feedback e melhorias" no README, rodapé do `/sdd` e regra na constituição gerada; issues públicas no repositório do plugin, sem segredo, log bruto, `.env` ou dado pessoal.
- Setup lista todo plugin recomendado ausente com comando de instalação, fonte oficial e o que degrada sem ele (`hooks/check-plugins.py`, leitura local, nunca instala; "não verificado" vira pendência, nunca presente); a lista vive na tabela "Plugins de terceiros: instalação" de `base/skills-padrao.md`.
- Setup explica a proteção de segredo camada por camada (hook local bloqueia commit; CI reporta; só required check bloqueia merge, e depende de plano e visibilidade) e grava pendência `required-check-gitleaks` com o comando para a própria pessoa verificar.

Corrige:

- Payload sem caminho que só existe no repositório de origem do framework: mensagens dos hooks, comentários do `.gitleaks.toml` e do `gitleaks.yml`, `base/fluxo-sdd.md`, `base/skills-padrao.md`, agente reviewer e README reescritos por efeito no adotante; gate de release passa a acusar reintrodução.
- Cartões `dados-de-ia.md` e `observabilidade.md` sem stack afirmada como fato; decisões preservadas.
- Constituição-template sem stack afirmada: política de acesso imposta no banco (RLS ou equivalente da stack declarada), política do banco ligada, nunca operar infraestrutura própria no lugar do serviço gerenciado declarado; 119 linhas mantidas.
- CHANGELOG da fonte com hash real nas versões 0.2.1 e 0.3.0 e cabeçalho que declara o `INTEGRIDADE.txt` da tag como autoridade.

Integridade: sha256:a5c1b66df3d57221e640878d944c4a9df5ee70791ed60848ffe8a5511ba1a8ac (amarração 0.4.0 → hash; conjunto do pacote, excluindo CHANGELOG.md e INTEGRIDADE.txt).

## 0.3.0 — 2026-08-16

Classificação: minor (adiciona sem quebrar; o pacote passa a entregar tudo o que o contrato distribuído cita).

Adiciona:

- Seed do mapa do sistema, `base/templates/mapa-do-sistema-template.md`: memória estrutural entre fatias, criado pela primeira fatia com código em `specs/_arquitetura/mapa-do-sistema.md`.
- Cartões de padrão de engenharia em `base/padroes/`, lidos pelo adotante em `docs/padroes/`, como a constituição-template e o 03-plan já citavam:
  - `dados-de-ia.md`
  - `evals-de-ia.md`
  - `observabilidade.md`
- Constituição-template pós-fatia 004: princípio de fronteira declarada antes de código e contexto mínimo emendado.
- Templates 03-plan e 04-tasks com a seção "Fronteiras e módulos" e a atualização do mapa como passo da fatia; mandatos de architect, spec-writer, implementer e reviewer com o mapa e as fronteiras.
- Duas linhas na tabela de cópia do sdd-setup: `templates/` passa a levar o seed para `specs/_templates/`; `padroes/*.md` vai para `docs/padroes/` (copy-if-absent).
- Gate 2 do empacote com completude: todo `*.md` de primeiro nível dos diretórios distribuíveis está no pacote, byte-idêntico à fonte, e toda citação de destino do adotante resolve para arquivo do pacote.
- Gate 5 endurecido: a entrada do topo do CHANGELOG precisa carregar a linha `Integridade:`; sem ela, o empacote para em vez de gravar o hash na versão anterior.
- Teste negativo do gate de completude versionado e rodando no CI de PR.

Integridade: sha256:3b90256b1eb75a1dae454483d330fa6cfdae0615f3a4c25befc6b3086b764857 (amarração 0.3.0 → hash; conjunto do pacote, excluindo CHANGELOG.md e INTEGRIDADE.txt).

## 0.2.1 — 2026-08-15

Classificação: patch (corrige entrega de contrato e defeito de release; as adições são texto de instrução das correções do Veredito).

Corrige:

- Regra de retomada por nomes de artefato (tabela dos quatro casos) agora vive na skill do condutor distribuída, não só no plano (C1 do Veredito).
- Empacote grava a amarração semver → hash só na entrada corrente do CHANGELOG, preservando as amarrações históricas (C3); push do release atômico (main e tag juntos); gate de rede cobre também `*.yml`/`*.yaml`, com a exceção do workflow do gitleaks registrada e justificada.
- `/sdd` nomeia o caminho do registro da entrevista (`docs/decisoes/*-setup-sdd.md`) ao enumerar pendências e ganha fallback sem registro: só o id, apontando a skill sdd-setup, nunca pergunta improvisada.
- Retomada da entrevista usa o MESMO arquivo de registro da primeira execução; nunca nasce um segundo registro.

Adiciona:

- Instrução de ativação do AX no projeto adotante: cópia de `agents/_engatilhados/` para `.claude/agents/`, no arquivo do agente e na skill do condutor.
- Seção "Voltar de versão" no README: rollback é roll-forward por tag nova do workflow; edição manual do repositório de distribuição é proibida.
- Pendência rastreável do design system quando a resposta é "não tenho": issue "Criar design system na primeira fatia com UI" com GitHub disponível; sem GitHub, entrada no roadmap inicial (arbitragem do portão de Veredito).

Integridade: sha256:8caf3b287fe5574e94e4c6ff45ebc298d6047f5e10a64032e02403bd2b17e429 (amarração 0.2.1 → hash; conjunto do pacote, excluindo CHANGELOG.md e INTEGRIDADE.txt).

## 0.2.0 — 2026-08-15

Classificação: minor (adiciona sem quebrar; inclui uma correção de texto).

Adiciona:

- Lacuna `design-system` na constituição-template (a camada de Integrações fica só com integrações e serviços alugados).
- Camada design system na entrevista de setup (bloco 3, agora nove camadas), com "não tenho" gravando texto fixo da skill e "não sei" virando pendência.
- Mandato do ux-architect orientado pelo design system declarado na constituição, não por nome fixo; sem declaração, a primeira fatia com UI cria o do projeto.
- Regra do implementer: front-end, relatório e dashboard seguem o design system declarado; componente fora do padrão é desvio.

Corrige:

- Parser da linha de origem no `/sdd`: regex ancorada `itxpro-sdd@X.Y.Z`, sem capturar pontuação vizinha (achado A2 do teste de adoção).

Integridade: sha256:1a1a27ef536ba5c8198c32213d99a6dc83b7d051d314169d1dafcaac25b5b62f (amarração 0.2.0 → hash; conjunto do pacote, excluindo CHANGELOG.md e INTEGRIDADE.txt).

## 0.1.0 — 2026-08-15

Classificação: minor (primeira versão distribuída; tudo é adição, nada quebra).

Entrega:

- Comando `/sdd`, despachante único do pipeline.
- Skill `sdd-setup`: entrevista em seis blocos, preenchimento da constituição por lacuna com id, registro append-only da entrevista, esqueleto por cópia.
- Skill `sdd-conductor` e os nove agentes das mesas.
- Hooks de enforcement via `hooks.json`: gate de segredo em commit (fail-closed), aviso de implementação sem spec aprovada, teto de 120 linhas da constituição. Regras hookify no payload de setup.
- Payload `base/`: constituição-template com sintaxe de lacuna, templates numerados 01 a 06, fluxo SDD, diagrama do pipeline, `.gitleaks.toml` e workflow de CI do gitleaks.

Integridade: sha256:051e6958611b8c8322b8ce91ab4bb2ee02e6f6f52058419f9cf66ce176114292 (amarração 0.1.0 → hash; conjunto do pacote, excluindo CHANGELOG.md e INTEGRIDADE.txt).
