# Changelog — itxpro-sdd

Régua de versão, pela ótica do contrato que o agente adotante lê: major quebra nome, caminho ou instrução existente; minor adiciona sem quebrar; patch corrige texto.

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

Integridade: gravado no release (hash SHA-256 do conjunto de arquivos e amarração semver → hash; o gate 5 do empacote confere).

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
