---
name: sdd-setup
description: Use no setup de um projeto novo com o framework SDD, logo após instalar o plugin. Conduz a entrevista em seis blocos, preenche a constituição (CLAUDE.md) e instancia o esqueleto do projeto. Não use para conduzir fatia; isso é o sdd-conductor, via /sdd.
---

# Setup do projeto SDD

Você conduz o setup: entrevista a pessoa, preenche a constituição e copia o esqueleto do pacote. Você não inventa conteúdo. O que a pessoa não respondeu fica declarado como pendência.

Fixe o locale em todo comando de contrato desta skill: `export LC_ALL=en_US.UTF-8`.

## Passo 0 — Pré-requisitos

Rode `sh "${CLAUDE_PLUGIN_ROOT}/hooks/check-prereqs.sh"` antes de qualquer outra coisa.

- **gitleaks ausente ou abaixo de 8.21.0**: imprima o comando de instalação que o check sugere, recomende verificar o checksum do binário contra o release oficial, e PARE. A pessoa instala e roda o setup de novo.

> É proibido ao agente executar o download ou a instalação do gitleaks. A skill imprime o comando e devolve a execução à pessoa. Sem gitleaks, o gate de commit é fail-closed: commit nenhum passa.

Depois, rode `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/check-plugins.py"`. Ele lê a tabela "Plugins de terceiros: instalação" de `${CLAUDE_PLUGIN_ROOT}/base/skills-padrao.md` e o registro local de plugins instalados (leitura somente); imprime, para cada ausente, o comando de instalação, a fonte oficial e o que degrada sem ele. Você não instala nada e não roda o comando impresso: repita a lista no fechamento e no registro da entrevista como pendência "plugin ausente: <nome>", com o comando ao lado. Se o script disser "não verificado", a lista inteira entra como não verificada (pendência "plugins não verificados: confira com /plugin"), nunca como presente. Nenhum plugin da tabela é pré-requisito: o setup continua.

- **Plugin recomendado ausente (lista do check-plugins)**: continue o setup e declare a ausência como pendência no fechamento e no registro da entrevista. Ausência nunca vira silêncio.

## A entrevista

Abertura, em cinco linhas:

1. Vou configurar o SDD neste projeto: preencho a constituição e crio o esqueleto.
2. São seis blocos de perguntas, uns 15 minutos.
3. "Não sei" vale como resposta e fecha o item na hora. Dá pra parar e retomar depois: o progresso vive no arquivo.
4. As respostas vivem em arquivos deste repositório, com duas exceções: a do design system e a do required check do gitleaks podem virar issue no rastreador deste mesmo repositório, aberta com a sua credencial e visível a quem enxerga o repositório. Nenhuma resposta vai para a ITXPRO nem para terceiro.
5. Não cole credencial, chave, connection string, token, nem dado pessoal de cliente real. Responda com categorias, não com exemplos reais.

Anuncie o progresso a cada bloco ("Bloco 3 de 6"). As regras abaixo valem a entrevista inteira.

> **Regras invioláveis (ux).** Toda pergunta com default aceita confirmação de uma palavra. Todo bloco aceita "aceitar o bloco inteiro". "Não sei" fecha o item na hora, sem insistência.

> **Anti-autopreenchimento (AX).** Nunca preencha lacuna com valor que a pessoa não deu. Sugestão mora na pergunta, escolha mora na resposta. É proibido inferir resposta de git config, de arquivo do repo, de outra resposta ou de conhecimento geral. Sem resposta, o item vira PENDENTE, nunca valor plausível. Grave o par pergunta → resposta no registro da entrevista antes de gravar na constituição. Nunca grave resposta que contenha "[[LACUNA:".

> **Higiene (security).** Não cole credencial, chave, connection string, token, nem dado pessoal de cliente real. Categorias, não exemplos reais. Resposta com cara de segredo (padrões do `.gitleaks.toml`) não é gravada: descarte e peça reformulação. As respostas só vivem em arquivos sob a raiz do repositório do adotante, com duas exceções: a do design system e a do required check do gitleaks podem virar issue no rastreador dele, em texto fixo que carrega o fato da resposta e nunca as palavras da pessoa.

Repita o aviso de higiene, na íntegra, antes do Bloco 2 (dado) e antes do Bloco 3 (stack).

### Os seis blocos e os ids que preenchem

A pergunta e o exemplo de cada id vivem na própria lacuna do template. Faça a pergunta da lacuna, com o exemplo como default quando couber.

| Bloco | Tema | Ids do template |
|---|---|---|
| 1 de 6 | Identidade | `nome-projeto`, `descricao-produto`, `diferencial-negocio`, `referencia-estilo` |
| 2 de 6 | Domínio e dado | `fonte-dado-dominio`, `dado-sensivel-dominio`, `papeis-projeto`, `nunca-do-dominio` |
| 3 de 6 | Stack por camada | `stack-linguagem`, `stack-backend`, `stack-web`, `stack-mobile`, `stack-integracoes`, `topologia-dado`, `topologia-aplicacao`, `topologia-pipeline`, `design-system` |
| 4 de 6 | Conhecimento e agentes | nenhum id; respostas vão só ao registro |
| 5 de 6 | Compliance | `compliance-especifico` |
| 6 de 6 | Fechamento | `versao-plugin` (automática, nunca perguntada) |

- **Bloco 1**: do fácil pro denso. Nome, produto, diferencial, estilo de escrita.
- **Bloco 2**: três a quatro abertas, cada uma com o exemplo da lacuna. Aviso de higiene antes.
- **Bloco 3**: aviso de higiene antes. Para cada camada, apresente o default do template, uma alternativa e um insight de uma frase no formato "X te serve até Y; troque se Z". Aceite por camada em uma palavra; "aceitar o bloco inteiro" fecha as nove camadas de uma vez. Na camada `design-system`, resposta "não tenho" grava este texto fixo (vem da skill, não é geração): `Sem design system definido. A primeira fatia com UI cria o do projeto em specs/_design-system/ e ele passa a reger daí em diante.` Junto, registre a pendência de forma rastreável (arbitragem do portão de Veredito da fatia 003): com GitHub disponível no projeto, abra a pendência `design-system` pelo passo "Issues das pendências do setup", que a faz nascer rotulada; sem GitHub, acrescente essa pendência ao `docs/roadmap.md` inicial. "Não sei" grava PENDENTE como qualquer id. Pergunta da camada, no ritmo desenhado: "Camada design system: o projeto já tem um design system definido? Se sim, diga qual e onde vive (repositório, pacote ou URL dos tokens). Ex.: tokens e CSS no repositório acme-designsystem. 'Não tenho' vale e fecha a camada: a primeira fatia com UI cria o do projeto. Insight: design system declarado vira o guia do ux-architect e das demais vozes em telas, relatórios e dashboards."
- **Bloco 4**: o projeto tem base de conhecimento pra RAG? Existe MCP de acesso a dado? Quais outros MCPs os agentes usam? Nenhuma lacuna no template: a resposta vai ao registro da entrevista e o que exigir decisão vira pendência declarada lá.
- **Bloco 5**: LGPD é afirmação, não pergunta: a constituição já a assume (contexto Brasil). Pergunte o compliance específico com o menu único abaixo. Múltipla escolha; "nenhum" e "não sei" valem.
- **Bloco 6**: fechamento (seção Término).

Menu de compliance, uma linha de "quando se aplica" cada:

- NIST CSF 2.0: quando a empresa organiza o programa de segurança por funções, de governar a recuperar.
- NIST AI RMF: quando o produto usa IA e o risco de IA precisa de gestão nomeada.
- ISO 42001: quando a empresa quer certificar o sistema de gestão de IA.
- ISO 27001: quando cliente ou contrato exige certificação de gestão de segurança da informação.
- GDPR: quando o produto trata dado de pessoa na União Europeia.
- EU AI Act: quando o produto opera ou vende sistema de IA na União Europeia.
- SOC 2: quando cliente B2B pede relatório de controles de confiança.
- CIS Controls: quando o time quer uma lista priorizada e prática de controles técnicos.
- COBIT: quando a governança de TI corporativa exige framework formal.
- ITIL: quando a operação de serviço de TI segue processos formais de incidente e mudança.

## Mecânica de preenchimento

1. Grave o par pergunta → resposta literal no registro da entrevista (abaixo), por id.
2. Em seguida substitua a lacuna inteira (`[[LACUNA:id | ... ]]`) no `CLAUDE.md` do projeto pela resposta, imediatamente. Uma resposta, uma gravação: o disco é o progresso.
3. "Não sei" grava `(PENDENTE:id — o adotante decide depois)` no ponto exato da lacuna.
4. Escape na gravação: se a resposta contém "[[", grave com um espaço entre os colchetes ("[ ["). Resposta contendo "[[LACUNA:" não é gravada de forma nenhuma: peça reformulação.
5. `versao-plugin`: leia o campo `version` de `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` e grave sem perguntar. É a linha de origem da constituição; atualização futura do plugin não a reescreve.

Registro da entrevista: `docs/decisoes/AAAA-MM-DD-setup-sdd.md`, com a data da PRIMEIRA execução. Append-only: nunca reescreva entrada existente. Retomada acrescenta ao fim do MESMO arquivo; nunca crie um segundo registro com data nova. Cada entrada tem o id, a pergunta feita e a resposta literal. O diff entre template e constituição precisa ser bijetivo com esse registro: trecho alterado sem par registrado é palpite.

## O esqueleto

> Esqueleto só nasce de cópia do pacote ou de lacuna preenchida, nunca de geração. Se você está redigindo conteúdo que não veio do pacote nem de resposta da pessoa, pare.

Cópia é copy-if-absent: arquivo que já existe no projeto nunca é sobrescrito; reporte e siga. Origem `${CLAUDE_PLUGIN_ROOT}/base/`:

| Origem (base/) | Destino no projeto |
|---|---|
| `constituicao-template.md` | `CLAUDE.md` (preenchido pela entrevista) |
| `templates/` (01-spec, 03-plan, 04-tasks, mapa-do-sistema-template) | `specs/_templates/` |
| `padroes/*.md` (cartões de padrão de engenharia) | `docs/padroes/` |
| `skills-padrao.md` | `docs/skills-padrao.md` |
| `fluxo-sdd.md` | `docs/fluxo-sdd.md` |
| `diagrama-pipeline-sdd.svg` | `docs/diagrama-pipeline-sdd.svg` |
| `hookify/*.local.md` | `.claude/` |
| `.gitleaks.toml` | raiz do projeto |
| `gitleaks.yml` | `.github/workflows/gitleaks.yml` |

Quando `gitleaks.yml` for copiado ou já existir no destino, imprima este texto fixo da skill, na íntegra:

> Proteção de segredo neste repositório, camada por camada: (1) o hook local do plugin bloqueia o `git commit` com segredo executado pelo agente nesta sessão do Claude Code (PreToolUse sobre Bash), fail-closed, na sua máquina; commit que você faz no seu terminal não passa por ele; (2) o workflow `.github/workflows/gitleaks.yml` varre o histórico no CI e reporta falha no job; (3) só um required check bloqueia o merge, e required check depende do plano e da visibilidade do repositório no GitHub (repositório privado em plano Free não tem required check). Nenhuma camada dessas é ativada por mim: a (1) e a (2) vêm com o esqueleto; a (3) é configuração sua no GitHub.

Em seguida, uma pergunta opcional, resposta fechada: "Este repositório é privado e está em plano Free? sim / não / não sei." Um destino por resposta:

- "Não" → registro da entrevista: "required check disponível; recomendação: marcar o job do gitleaks como required check nas regras do branch padrão".
- "Sim", "não sei" ou sem resposta → PENDENTE `required-check-gitleaks` no registro da entrevista, com a recomendação (required check quando o plano permitir, ou repositório público) e os comandos para a própria pessoa verificar, cada um com alvo explícito: `gh repo view <dono>/<repositório> --json isPrivate,visibility` e `gh api user --jq .plan.name` (organização: `gh api orgs/<org> --jq .plan.name`). O `<dono>/<repositório>` é o do `origin` do checkout, e ele vai escrito porque chamada sem alvo resolve o repositório pelo diretório corrente, que é o repositório errado sempre que o diretório for outro; `api user` e `api orgs/<org>` não são de repositório e já carregam o alvo que têm. Você não roda esses comandos nem infere a resposta de arquivo, remoto ou git config: a regra de anti-autopreenchimento vale aqui, e é ela que faz o alvo ficar em marcador para a pessoa preencher em vez de o rito ler o remoto. A pendência segue o mesmo rito do design system: com GitHub no projeto, abra a pendência `required-check-gitleaks` pelo passo "Issues das pendências do setup", que a faz nascer rotulada; sem GitHub, linha no `docs/roadmap.md` inicial. Ela aparece no fechamento junto das demais pendências.

Crie também, vazios de conteúdo gerado: `docs/decisoes/` (recebe o registro da entrevista) e `docs/roadmap.md` inicial. A roadmap nasce com o título, a tabela de quatro colunas e a legenda, e sem nenhuma linha de fatia: as fatias entram pela mesa de Intenção. Grave este texto fixo (vem da skill, não é geração):

```md
# Roadmap

| Estado | Ordem | Candidata | Issues |
|---|---|---|---|

> Estado, vocabulário fechado: `prevista`, aceita na fila e nenhuma fase começou; `em curso`, alguma fase aberta, da Intenção ao Veredito; `entregue`, integrada ao branch padrão; `arquivada`, saiu da fila sem entrega, com o motivo na própria linha.
```

A célula `Estado` aceita um desses quatro tokens e mais nada: sem sinônimo, sem prosa, um token por linha. Publicação não entra no vocabulário, porque o CHANGELOG e a tag já a registram. Pendência que o setup acrescenta à roadmap (design system, required check) entra como linha de prosa abaixo da tabela, nunca como linha da tabela: pendência não é fatia, e a coluna `Estado` é do ciclo de vida da fatia. Os hooks nativos não se copiam: vêm do plugin, via `hooks.json`.

### Rótulos de prioridade do backlog

A constituição manda que toda issue nasça rotulada com uma das três labels de prioridade, e a regra só se cumpre se as três existirem no repositório. É o setup que as cria: `P0`, `P1` e `P2`, uma vez, no esqueleto. Rode o fence abaixo dentro do checkout do projeto e repita a saída dele no fechamento.

Ele cria o que falta e não toca no que já está lá. Rótulo que já existe é do adotante, com a cor e a descrição que ele escolheu, e o setup não é dono disso: sem `--force`, sem editar e sem remover. Idempotência que muta é idempotência falsa.

**A leitura vem antes da criação, e custa uma chamada a mais sempre.** O outro caminho seria disparar as três criações e deixar o erro dizer qual já existia, sem leitura nenhuma. Ele custa uma chamada a menos e paga em outra moeda: a criação devolve o mesmo código de saída para "já existe" e para "não tenho permissão", e o que separa os dois é a frase da ferramenta, que muda de versão e de idioma. Dizer "encontrei" em cima de um erro de permissão é afirmar o que não foi medido.

**Leitura que não responde não vira criação às cegas.** Sem a lista, nada nasce: o passo diz em uma linha que não leu, deixa a pendência e devolve a decisão à pessoa. O custo fica declarado em vez de escondido, e ele é real: até alguém criar os três à mão ou rodar o passo de novo com uma credencial que leia, a regra do backlog fica sem com o que ser cumprida naquele repositório. Criar às cegas seria o mesmo palpite que o anti-autopreenchimento proíbe, com efeito num repositório de verdade.

**Encontrar é resultado, não silêncio.** Cada rótulo que já existia sai em uma linha dizendo que ficou como estava. Passo que não faz nada e não diz nada é indistinguível de passo que não rodou.

```bash
# Rótulos de prioridade do backlog do adotante: P0, P1 e P2. Roda uma vez, no
# esqueleto, dentro do checkout do projeto. CRIA o que falta e não toca no que
# existe: nem nome, nem cor, nem descrição. Sem `--force`, sem o verbo que edita
# e sem o que remove. Os três mudariam rótulo de quem adota, e mudar é o oposto
# de criar o que falta.
set -u
export LC_ALL=en_US.UTF-8

# O ALVO SAI DO `origin` DESTE CHECKOUT, nunca de literal, e viaja explícito em
# cada chamada. Chamada sem alvo resolve o repositório pelo diretório corrente,
# e este passo roda na máquina de quem adota: diretório errado cria rótulo na
# casa de outra pessoa. Origin ausente, ou fora da forma `dono/repositório`, é
# argumento que não dá para medir, e não medir sai dito em vez de virar chamada
# ao acaso.
# A AUTORIDADE SE SEPARA NA PRIMEIRA BARRA E SE PODA ATÉ O ÚLTIMO ARROBA. A
# autoridade do git termina no ÚLTIMO arroba: com usuário em forma de e-mail,
# que é a forma comum em host corporativo, cortar no primeiro devolve o resto do
# userinfo, com a senha em claro. E o HOST não se descarta: sem ele o destino da
# chamada seria `dono/repositório` sozinho, e quem escolheria a máquina era a
# variável de ambiente de quem roda. `GH_HOST` exportado aqui fixa o destino no
# host do `origin` e apaga o que veio de fora, em toda chamada deste passo.
URL=$(git remote get-url origin 2>/dev/null) || exit 70
ALVO=${URL%.git}
ALVO=${ALVO%/}
HOST=
case "$ALVO" in
  *://*)
    ESQUEMA=${ALVO%%://*}
    RESTO=${ALVO#*://}
    HOST=${RESTO%%/*}                  # autoridade: para na primeira barra
    HOST=${HOST##*@}                   # userinfo fora, até o ÚLTIMO arroba
    case "$ESQUEMA" in
      http|https) ;;                   # porta que navega é porta da API
      *) HOST=${HOST%%:*} ;;           # porta de transporte não é de API
    esac
    case "$RESTO" in
      */*) ALVO=${RESTO#*/} ;;
      *)   ALVO= ;;                    # autoridade sem caminho: não medi
    esac
    ;;
  *:*)
    HOST=${ALVO%%:*}                   # forma scp: `git@host:dono/repo`
    HOST=${HOST##*@}
    ALVO=${ALVO#*:}
    ;;
esac
case "$HOST" in
  '' | *[!A-Za-z0-9._:-]*)
    printf 'não consegui derivar o host do `origin` deste checkout, e sem host o destino viria do ambiente: nada foi criado\n'
    exit 70 ;;
esac
case "$ALVO" in
  */*/*)
    printf 'o `origin` deste checkout não deriva para a forma `dono/repositório`, que é a única que a ferramenta endereça: nada foi criado\n'
    exit 70 ;;                         # caminho, não `dono/repositório`
  ?*/?*) ;;
  *)
    printf 'o `origin` deste checkout não deriva para a forma `dono/repositório`, que é a única que a ferramenta endereça: nada foi criado\n'
    exit 70 ;;
esac
export GH_HOST="$HOST"

# UMA LEITURA SÓ, e ela vem antes de qualquer criação. Saber pela falha da
# criação custaria esta chamada a menos e devolveria o mesmo código para "já
# existe" e para "não tenho permissão": o que separa os dois é a frase da
# ferramenta, e frase muda de versão e de idioma. O teto de 200 é a página que
# cobre repositório real; nome que ficasse fora dela vira tentativa de criação
# que a ferramenta recusa, e a recusa sai dita, nunca em cima do que já existe.
EXISTENTES=$(gh label list --repo "$ALVO" --limit 200 --json name --jq '.[].name' 2>/dev/null)
LIDO=$?

# LEITURA QUE NÃO RESPONDE É FAIL-CLOSED: nada nasce, e o custo sai dito. Sem os
# três rótulos, a regra do backlog fica sem com o que ser cumprida neste
# repositório, e é por isso que a linha vira pendência do fechamento em vez de
# sumir.
if [ "$LIDO" -ne 0 ]; then
  printf 'rótulos de prioridade: não li os rótulos deste repositório, e por isso não criei nenhum\n'
  printf 'pendência rotulos-prioridade: crie P0, P1 e P2 à mão, ou rode este passo de novo com uma credencial que leia o repositório\n'
  exit 91
fi

# Linha inteira, nunca pedaço: `P1` não casa com `P10` nem com `prioridade P1`.
ja_existe() { printf '%s\n' "$EXISTENTES" | grep -qxF "$1"; }
# ENCONTRAR E NÃO CRIAR É RESULTADO, NÃO SILÊNCIO.
achei() { printf 'rótulo %s: já existe neste repositório, mantido como está, com a cor e a descrição de quem o criou\n' "$1"; }
criei() { printf 'rótulo %s: criado\n' "$1"; }
FALTOU=0
nao_criei() { printf 'rótulo %s: a criação não foi aceita, e nada foi alterado\n' "$1"; FALTOU=1; }

# OS TRÊS NOMES VÃO LITERAIS, um `gh label create` por rótulo. Em laço sobre uma
# variável o nome some do texto, e régua nenhuma que leia o pacote alcança o
# vocabulário que o kit cria no repositório de quem adota. Literal custa três
# blocos parecidos; variável custa a régua.
if ja_existe P0; then
  achei P0
elif gh label create "P0" --repo "$ALVO" --color b60205 \
       --description "fura a fila do roadmap" >/dev/null 2>&1; then
  criei P0
else
  nao_criei P0
fi

if ja_existe P1; then
  achei P1
elif gh label create "P1" --repo "$ALVO" --color fbca04 \
       --description "entra na próxima janela" >/dev/null 2>&1; then
  criei P1
else
  nao_criei P1
fi

if ja_existe P2; then
  achei P2
elif gh label create "P2" --repo "$ALVO" --color 0e8a16 \
       --description "espera agrupamento" >/dev/null 2>&1; then
  criei P2
else
  nao_criei P2
fi

[ "$FALTOU" -eq 0 ] || exit 92
exit 0
```

Os três nomes vão literais na chamada, um `gh label create` por rótulo, nunca em laço sobre uma variável. Com o nome em variável, régua de texto nenhuma alcança o vocabulário que o kit cria no repositório de quem adota, e a garantia de que rótulo de processo interno não viaja passa a depender só da suíte que exercita o passo. O preço do literal é a repetição de três blocos parecidos, e ele é o menor dos dois.

Códigos de saída do passo, e cada um nomeia o que mediu: `0`, os três existem, criados agora ou encontrados; `70`, o `origin` deste checkout não deriva para `dono/repositório` e nenhuma chamada saiu; `91`, não deu para ler os rótulos e nada foi criado; `92`, a leitura respondeu e alguma criação não foi aceita, sem nada alterado.

### Issues das pendências do setup

Duas pendências do setup viram issue no repositório de quem adota: a do design system, quando a camada `design-system` fecha em "não tenho", e a do required check do gitleaks, quando a pergunta do plano fecha em "sim", "não sei" ou sem resposta. As duas nascem **rotuladas**, pela regra do backlog que a constituição do projeto carrega na seção Gestão de trabalho: rótulo é condição de nascimento da issue, nunca acerto posterior. Rode o fence abaixo depois do passo dos rótulos, dentro do checkout, com os ids desta execução, e repita a saída no fechamento. Sem GitHub no projeto nada disto roda, e as duas pendências entram como linha de prosa no `docs/roadmap.md` inicial.

**Qual rótulo cada uma recebe, e pelo gatilho, nunca pela importância que ela aparenta.** Os três nomeiam QUANDO o trabalho entra.

- **Required check do gitleaks: `P1`, entra na próxima janela.** Falta uma marcação nas regras do branch padrão e nada no produto o bloqueia, então o trabalho está pronto para hoje. Não espera agrupamento porque não há com o que agrupar.
- **Design system: `P2`, espera agrupamento.** Quem o cria é a primeira fatia com UI, que pode ser a próxima ou pode demorar. `P1` agendaria para a próxima janela um trabalho cuja entrada não nasceu.

**Nenhuma das duas fura a fila.** `P0` no dia do setup ordena o roadmap de um projeto que ainda não tem fatia. A do gitleaks é a que mais puxa para lá, e o que a segura é que as camadas (1) e (2) já vieram com o esqueleto e que a ativação pode estar fora do alcance de quem adota até o plano mudar: prioridade que a pessoa não tem como cumprir no dia em que a recebe é ruído.

**A leitura vem antes da criação.** Criar primeiro e rotular depois deixaria issue órfã no repositório alheio se o segundo passo falhasse, e a atomicidade da ferramenta não foi medida. Leitura que não responde é fail-closed: nada nasce e o passo diz em uma linha o que não leu. Ele repete a leitura do passo dos rótulos de propósito, porque passo que confia no que outro leu afirma o que não mediu. Limite declarado: o passo não pergunta se a issue já existe, então quem rodar o setup duas vezes abre a segunda cópia e fecha a duplicada à mão.

```bash
# Issues das duas pendências do setup, já ROTULADAS. Roda uma vez, no esqueleto,
# dentro do checkout, DEPOIS do passo dos rótulos, e recebe os ids desta
# execução: `design-system`, `required-check-gitleaks`, ou os dois.
set -u
export LC_ALL=en_US.UTF-8

# O ALVO SAI DO `origin` DESTE CHECKOUT, como no passo dos rótulos, e aqui errar
# custa mais: issue na casa de outra pessoa manda e-mail, e e-mail não se desfaz.
# A AUTORIDADE SE SEPARA NA PRIMEIRA BARRA E SE PODA ATÉ O ÚLTIMO ARROBA. A
# autoridade do git termina no ÚLTIMO arroba: com usuário em forma de e-mail,
# que é a forma comum em host corporativo, cortar no primeiro devolve o resto do
# userinfo, com a senha em claro. E o HOST não se descarta: sem ele o destino da
# chamada seria `dono/repositório` sozinho, e quem escolheria a máquina era a
# variável de ambiente de quem roda. `GH_HOST` exportado aqui fixa o destino no
# host do `origin` e apaga o que veio de fora, em toda chamada deste passo.
URL=$(git remote get-url origin 2>/dev/null) || exit 70
ALVO=${URL%.git}
ALVO=${ALVO%/}
HOST=
case "$ALVO" in
  *://*)
    ESQUEMA=${ALVO%%://*}
    RESTO=${ALVO#*://}
    HOST=${RESTO%%/*}                  # autoridade: para na primeira barra
    HOST=${HOST##*@}                   # userinfo fora, até o ÚLTIMO arroba
    case "$ESQUEMA" in
      http|https) ;;                   # porta que navega é porta da API
      *) HOST=${HOST%%:*} ;;           # porta de transporte não é de API
    esac
    case "$RESTO" in
      */*) ALVO=${RESTO#*/} ;;
      *)   ALVO= ;;                    # autoridade sem caminho: não medi
    esac
    ;;
  *:*)
    HOST=${ALVO%%:*}                   # forma scp: `git@host:dono/repo`
    HOST=${HOST##*@}
    ALVO=${ALVO#*:}
    ;;
esac
case "$HOST" in
  '' | *[!A-Za-z0-9._:-]*)
    printf 'não consegui derivar o host do `origin` deste checkout, e sem host o destino viria do ambiente: nada foi criado\n'
    exit 70 ;;
esac
case "$ALVO" in
  */*/*)
    printf 'o `origin` deste checkout não deriva para a forma `dono/repositório`, que é a única que a ferramenta endereça: nada foi criado\n'
    exit 70 ;;                         # caminho, não `dono/repositório`
  ?*/?*) ;;
  *)
    printf 'o `origin` deste checkout não deriva para a forma `dono/repositório`, que é a única que a ferramenta endereça: nada foi criado\n'
    exit 70 ;;
esac
export GH_HOST="$HOST"

# VOCABULÁRIO FECHADO DE ID, conferido antes de qualquer leitura. A recusa
# nomeia o vocabulário, nunca o que veio de fora.
QUER_DS=0
QUER_RC=0
for PEND in "$@"; do
  case "$PEND" in
    design-system) QUER_DS=1 ;;
    required-check-gitleaks) QUER_RC=1 ;;
    *)
      printf 'issues das pendências: id fora do vocabulário do passo, que é design-system e required-check-gitleaks, e nada foi criado\n'
      exit 70
      ;;
  esac
done
if [ "$QUER_DS" -eq 0 ] && [ "$QUER_RC" -eq 0 ]; then
  printf 'issues das pendências: nenhuma pendência nesta execução, e nada foi criado\n'
  exit 0
fi

# A LEITURA VEM ANTES DA CRIAÇÃO: o rótulo está aqui? Sem sim, nada nasce.
ROTULOS=$(gh label list --repo "$ALVO" --limit 200 --json name --jq '.[].name' 2>/dev/null)
LIDO=$?
if [ "$LIDO" -ne 0 ]; then
  printf 'issues das pendências: não li os rótulos deste repositório, e por isso não criei issue nenhuma\n'
  printf 'pendência issues-do-setup: rode este passo de novo com credencial que leia, ou abra as issues à mão, sempre rotuladas\n'
  exit 91
fi

tem_rotulo() { printf '%s\n' "$ROTULOS" | grep -qxF "$1"; }
criei() { printf 'issue %s: criada com o rótulo de prioridade\n' "$1"; }
SEM_ROTULO=0
sem_rotulo() { printf 'issue %s: o rótulo de prioridade dela não existe neste repositório, e sem ele a issue não nasce\n' "$1"; SEM_ROTULO=1; }
FALTOU=0
nao_criei() { printf 'issue %s: a criação não foi aceita, e nada foi criado\n' "$1"; FALTOU=1; }

# OS DOIS TÍTULOS E OS DOIS RÓTULOS VÃO LITERAIS, um `gh issue create` por
# pendência: em variável eles somem do texto, e régua nenhuma que leia o pacote
# alcança o que o kit escreve no repositório alheio. O corpo não monta link,
# porque link sairia do `origin` e `origin` pode carregar credencial.
if [ "$QUER_DS" -eq 1 ]; then
  if ! tem_rotulo P2; then
    sem_rotulo design-system
  elif gh issue create --repo "$ALVO" \
         --title "Criar design system na primeira fatia com UI" \
         --label "P2" \
         --body "Pendência do setup do SDD. O projeto não declarou design system, e a primeira fatia com UI cria o do projeto em specs/_design-system/." \
         >/dev/null 2>&1; then
    criei design-system
  else
    nao_criei design-system
  fi
fi

if [ "$QUER_RC" -eq 1 ]; then
  if ! tem_rotulo P1; then
    sem_rotulo required-check-gitleaks
  elif gh issue create --repo "$ALVO" \
         --title "Ativar required check do gitleaks quando o plano permitir" \
         --label "P1" \
         --body "Pendência do setup do SDD. O workflow do gitleaks já varre o histórico no CI, e falta marcar o job como required check nas regras do branch padrão. Depende do plano e da visibilidade deste repositório no GitHub." \
         >/dev/null 2>&1; then
    criei required-check-gitleaks
  else
    nao_criei required-check-gitleaks
  fi
fi

[ "$SEM_ROTULO" -eq 0 ] || exit 93
[ "$FALTOU" -eq 0 ] || exit 92
exit 0
```

Códigos de saída, e cada um nomeia o que mediu: `0`, as pendências pedidas nasceram; `70`, o `origin` não deriva para `dono/repositório` ou um id veio fora do vocabulário, e nenhuma chamada saiu; `91`, não li os rótulos e nada foi criado; `92`, a leitura respondeu e alguma criação não foi aceita; `93`, o rótulo da pendência não existe aqui e a issue não nasceu sem ele.

## Término e idempotência

Término da entrevista é fato mecânico, não interpretação:

```sh
export LC_ALL=en_US.UTF-8
! grep -qF '[[LACUNA:' CLAUDE.md
```

Enumeração, quando precisar listar o que falta (a pessoa nunca roda grep; você roda e apresenta):

```sh
grep -nE '\[\[LACUNA:[a-z0-9-]+[^]]*\]\]' CLAUDE.md   # lacunas restantes
grep -nE 'PENDENTE:[a-z0-9-]+' CLAUDE.md               # pendências por id
```

Fechamento (Bloco 6), nesta ordem:

1. Resumo por bloco, uma linha cada.
2. Pendências por id, com a pergunta original ao lado (a pergunta vive no registro da entrevista).
3. Plugins recomendados ausentes (ou não verificados), um por linha, com o comando de instalação ao lado; a instalação é da pessoa.
4. Varredura anunciada: rode `grep -rni itxpro CLAUDE.md`, ignorando só o padrão exato `itxpro-sdd@` da linha de origem e `itxpro-sdd-plugin` da regra de feedback; qualquer outro hit é erro de preenchimento, corrija com a pessoa.
5. Lista do que foi criado (arquivo por arquivo) e do que foi pulado por já existir.
6. Versão gravada: "constituição nascida do plugin itxpro-sdd@X.Y.Z".
7. Próximo passo único: "rode /sdd".

Re-execução da skill:

- `CLAUDE.md` com `[[LACUNA:` → retome só o que falta: enumere as lacunas restantes e pergunte só essas. Não refaça bloco fechado.
- `CLAUDE.md` sem `[[LACUNA:` → reporte a versão da linha de origem e ofereça revisar só os `(PENDENTE:`, por id. Nada mais é reaberto.
- Sem `CLAUDE.md` → setup do zero.

## Racionalizações já observadas

| Pensamento | Realidade |
|---|---|
| "O git config diz o nome, já preencho" | Inferência é palpite. Sugestão mora na pergunta, escolha mora na resposta. |
| "A pessoa hesitou, insisto mais uma vez" | "Não sei" fecha o item na hora. Pendência declarada vence resposta arrancada. |
| "Gero um roadmap inicial bem completo" | Esqueleto nasce de cópia ou de lacuna, nunca de geração. |
| "Instalo o gitleaks pra ela, é rápido" | Download é da pessoa. Você imprime o comando e para. |
| "Instalo o plugin que falta, é um comando" | Você imprime o comando; instalar é da pessoa. Ausente vira pendência, "não verificado" nunca vira presente. |
| "Confiro com `gh` se o repositório é privado" | Essa leitura não é sua e nada se infere: a pessoa responde ou o item vira PENDENTE com o comando para ela rodar. |
| "A resposta parece um token, mas deve ser exemplo" | Cara de segredo não se grava. Descarte e peça reformulação. |
| "O `P1` dele está com a cor errada, já corrijo" | Rótulo que já existe é do adotante. Encontrou, diz em uma linha e segue. |
| "Crio os três e vejo pelo erro qual já existia" | O erro não separa "já existe" de "não tenho permissão". Leia antes de criar. |
