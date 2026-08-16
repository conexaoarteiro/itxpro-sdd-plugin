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

- **Plugin hookify ou superpowers ausente**: continue o setup e declare a ausência como pendência no fechamento e no registro da entrevista. Ausência nunca vira silêncio.

## A entrevista

Abertura, em cinco linhas:

1. Vou configurar o SDD neste projeto: preencho a constituição e crio o esqueleto.
2. São seis blocos de perguntas, uns 15 minutos.
3. "Não sei" vale como resposta e fecha o item na hora. Dá pra parar e retomar depois: o progresso vive no arquivo.
4. Nada sai da sua máquina: as respostas só vivem em arquivos deste repositório.
5. Não cole credencial, chave, connection string, token, nem dado pessoal de cliente real. Responda com categorias, não com exemplos reais.

Anuncie o progresso a cada bloco ("Bloco 3 de 6"). As regras abaixo valem a entrevista inteira.

> **Regras invioláveis (ux).** Toda pergunta com default aceita confirmação de uma palavra. Todo bloco aceita "aceitar o bloco inteiro". "Não sei" fecha o item na hora, sem insistência.

> **Anti-autopreenchimento (AX).** Nunca preencha lacuna com valor que a pessoa não deu. Sugestão mora na pergunta, escolha mora na resposta. É proibido inferir resposta de git config, de arquivo do repo, de outra resposta ou de conhecimento geral. Sem resposta, o item vira PENDENTE, nunca valor plausível. Grave o par pergunta → resposta no registro da entrevista antes de gravar na constituição. Nunca grave resposta que contenha "[[LACUNA:".

> **Higiene (security).** Não cole credencial, chave, connection string, token, nem dado pessoal de cliente real. Categorias, não exemplos reais. Resposta com cara de segredo (padrões do `.gitleaks.toml`) não é gravada: descarte e peça reformulação. As respostas só vivem em arquivos sob a raiz do repositório do adotante.

Repita o aviso de higiene, na íntegra, antes do Bloco 2 (dado) e antes do Bloco 3 (stack).

### Os seis blocos e os ids que preenchem

A pergunta e o exemplo de cada id vivem na própria lacuna do template. Faça a pergunta da lacuna, com o exemplo como default quando couber.

| Bloco | Tema | Ids do template |
|---|---|---|
| 1 de 6 | Identidade | `nome-projeto`, `descricao-produto`, `diferencial-negocio`, `referencia-estilo` |
| 2 de 6 | Domínio e dado | `fonte-dado-dominio`, `dado-sensivel-dominio`, `papeis-projeto`, `nunca-do-dominio` |
| 3 de 6 | Stack por camada | `stack-linguagem`, `stack-backend`, `stack-web`, `stack-mobile`, `stack-integracoes`, `topologia-dado`, `topologia-aplicacao`, `topologia-pipeline` |
| 4 de 6 | Conhecimento e agentes | nenhum id; respostas vão só ao registro |
| 5 de 6 | Compliance | `compliance-especifico` |
| 6 de 6 | Fechamento | `versao-plugin` (automática, nunca perguntada) |

- **Bloco 1**: do fácil pro denso. Nome, produto, diferencial, estilo de escrita.
- **Bloco 2**: três a quatro abertas, cada uma com o exemplo da lacuna. Aviso de higiene antes.
- **Bloco 3**: aviso de higiene antes. Para cada camada, apresente o default do template, uma alternativa e um insight de uma frase no formato "X te serve até Y; troque se Z". Aceite por camada em uma palavra; "aceitar o bloco inteiro" fecha as oito camadas de uma vez.
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

Registro da entrevista: `docs/decisoes/AAAA-MM-DD-setup-sdd.md`, com a data do dia. Append-only: nunca reescreva entrada existente; retomada acrescenta ao fim. Cada entrada tem o id, a pergunta feita e a resposta literal. O diff entre template e constituição precisa ser bijetivo com esse registro: trecho alterado sem par registrado é palpite.

## O esqueleto

> Esqueleto só nasce de cópia do pacote ou de lacuna preenchida, nunca de geração. Se você está redigindo conteúdo que não veio do pacote nem de resposta da pessoa, pare.

Cópia é copy-if-absent: arquivo que já existe no projeto nunca é sobrescrito; reporte e siga. Origem `${CLAUDE_PLUGIN_ROOT}/base/`:

| Origem (base/) | Destino no projeto |
|---|---|
| `constituicao-template.md` | `CLAUDE.md` (preenchido pela entrevista) |
| `templates/` (01-spec, 03-plan, 04-tasks) | `specs/_templates/` |
| `skills-padrao.md` | `docs/skills-padrao.md` |
| `fluxo-sdd.md` | `docs/fluxo-sdd.md` |
| `diagrama-pipeline-sdd.svg` | `docs/diagrama-pipeline-sdd.svg` |
| `hookify/*.local.md` | `.claude/` |
| `.gitleaks.toml` | raiz do projeto |
| `gitleaks.yml` | `.github/workflows/gitleaks.yml` |

Crie também, vazios de conteúdo gerado: `docs/decisoes/` (recebe o registro da entrevista) e `docs/roadmap.md` inicial (título e uma linha: as fatias entram pela mesa de Intenção). Os hooks nativos não se copiam: vêm do plugin, via `hooks.json`.

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
3. Varredura anunciada: rode `grep -rni itxpro CLAUDE.md`, ignorando só o padrão exato `itxpro-sdd@` da linha de origem; qualquer outro hit é erro de preenchimento, corrija com a pessoa.
4. Lista do que foi criado (arquivo por arquivo) e do que foi pulado por já existir.
5. Versão gravada: "constituição nascida do plugin itxpro-sdd@X.Y.Z".
6. Próximo passo único: "rode /sdd".

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
| "A resposta parece um token, mas deve ser exemplo" | Cara de segredo não se grava. Descarte e peça reformulação. |
