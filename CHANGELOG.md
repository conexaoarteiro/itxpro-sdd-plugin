# Changelog — itxpro-sdd

Régua de versão, pela ótica do contrato que o agente adotante lê: major quebra nome, caminho ou instrução existente; minor adiciona sem quebrar; patch corrige texto.

O hash autoritativo de cada versão é o `INTEGRIDADE.txt` da tag correspondente no repositório de distribuição; a linha `Integridade:` aqui é cópia gravada após o release.

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
