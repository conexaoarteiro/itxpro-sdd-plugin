# Constituição do Projeto — [[LACUNA:nome-projeto | pergunta: qual o nome do projeto | ex.: plataforma de mentoria]]

> Fonte de verdade das regras do projeto. Todo agente lê este arquivo antes de agir. Quando uma regra aqui conflitar com sugestão de agente, esta constituição vence.
> Nascida do plugin: itxpro-sdd@[[LACUNA:versao-plugin | pergunta: preenchida automaticamente pelo setup com a versão do plugin.json, não pergunte à pessoa | ex.: 0.1.0]]. As lacunas deste arquivo são preenchidas na entrevista de setup.

## O que estamos construindo

[[LACUNA:descricao-produto | pergunta: descreva o produto em um parágrafo, o que é, pra quem e qual o objetivo central, nomeando o diferencial que só a sua empresa entrega | ex.: plataforma que conecta mentores e mentorados da empresa, com trilha e agenda integradas]]

## Princípios de produto (inegociáveis)

1. Uma fatia vertical por vez. Nada vai pra próxima fatia antes da anterior estar no ar e em uso. O roadmap em `docs/roadmap.md` é a ordem oficial.
2. Construir o fosso, alugar a commodity. O time só constrói o que é diferencial de [[LACUNA:diferencial-negocio | pergunta: qual o diferencial do negócio que o time constrói em vez de alugar | ex.: o motor de matching entre mentor e mentorado]]. O resto entra como serviço pronto, declarado na stack padrão.
3. O dado já existe. [[LACUNA:fonte-dado-dominio | pergunta: onde o dado do domínio já vive hoje | ex.: camada ouro do lakehouse, CRM, planilhas da operação]] O produto consome e organiza esse dado, não recria do zero.
4. Dado pessoal é dado sensível. Privacidade e controle de acesso não são fase posterior, entram em toda fatia desde a primeira.

## Princípios de engenharia (by design)

Estes princípios moldam o desenho desde o começo. Valem junto com os princípios de produto.

1. Privacy e security by design, proporcional ao risco. Toda fatia é classificada por sensibilidade de dado no início. A classificação calibra quanta cerimônia de segurança ela paga. Segurança molda o desenho, não só audita o resultado.
2. Experiência é cidadã de primeira classe, para humano e para agente. O produto é desenhado para a pessoa (UX e DEX) e para os agentes dos usuários (AX), com a mesma seriedade.
3. AI-first nos contratos. Todo contrato nasce consumível por agente, não só por tela. Expor superfície MCP é feature de fatia futura, mas a prontidão é princípio de agora.
4. Desempenho é orçamento explícito, na stack gerenciada. Cada plano declara um budget (latência, Core Web Vitals, plano de índice). A escala vem das alavancas da stack gerenciada, não de operar infra própria.
5. Segregação de função, com veto que sobrevive ao consenso. Quem desenha a restrição não é o único que a julga. A mesa converge onde dá e nomeia a divergência onde não dá. Veto continua veto.
6. Procedência antes de afirmação. Afirmação sobre o repo, o dado ou o domínio nasce de fonte verificada com ferramenta (`grep`, build, teste), não de memória. Nenhuma mesa fecha citando arquivo que ninguém abriu.
7. Artefato de registro imutável. Decisão registrada em `docs/decisoes/` não se reescreve. Entendimento novo gera nota nova, que referencia e supersede a antiga. O histórico fica auditável.
8. Lacuna declarada vence lacuna silenciosa. O que falta ou não foi decidido se escreve no artefato: questão aberta na spec, lacuna entre colchetes. Agente que encontra lacuna a declara, nunca a preenche por inferência.

## Fluxo de construção: três fases em mesa redonda

A construção de cada fatia passa por três fases. Transformação é processo com dono: cada fase tem condutor nomeado e artefato de saída registrado. Cada fase é uma mesa onde as vozes relevantes discutem, convergem e emitem uma decisão unificada. A sessão principal conduz a mesa, convoca cada agente, roda até duas rodadas de crítica cruzada, e sintetiza o artefato mais um registro de decisão curto.

1. Intenção. Mesa: spec-writer, security-privacy-architect, ux-architect. Saída: a spec, já com classificação de risco, intenção de experiência e postura AI-first. Portão humano, sempre.
2. Desenho. Mesa: architect, security-privacy-architect, ux-architect, devsecops. Saída: o plano e as tarefas, com controle de acesso, ameaça, interação, deploy e budget tecidos juntos. Portão por exceção: o desenho passa sozinho quando a mesa fecha sem bloqueio, e sobe ao humano só quando há divergência aberta ou veto.
3. Construção e veredito. O implementer constrói, uma tarefa por vez. Mesa de veredito: reviewer, grc-reviewer (veto), ux-architect, devsecops, e security-privacy-architect conforme o risco. Saída: um veredito único. Portão humano, sempre.

Regra da mesa: a decisão é unificada, mas o veto sobrevive ao consenso. O artefato que chega ao humano mostra a decisão e qualquer objeção dura que ficou de pé. Cada voz critica da sua ótica antes de convergir. Humano decide onde a máquina não alcança: portão humano não se delega a agente.

## Os agentes e o condutor

Oito agentes ativos: spec-writer, architect, security-privacy-architect, ux-architect, devsecops, implementer, reviewer, grc-reviewer (veto). Um engatilhado: agent-experience-architect (AX), em `agents/_engatilhados/`, que ativa quando a primeira fatia expuser MCP. O mandato de cada um vive no seu arquivo em `agents/`.

A sessão principal é o condutor do pipeline: convoca as mesas, sintetiza os artefatos e apresenta os portões ao dono do projeto. O condutor não implementa nem julga. O estado do pipeline vive em disco (`specs/NNN-*/`), nunca na conversa.

## Skills padrão

A constituição define o processo; as skills são a mecânica dentro das fases. O mapa de skills por agente e a regra de precedência vivem em `docs/skills-padrao.md`, herdados do framework. Quando uma skill conflitar com esta constituição, a constituição vence.

Os cartões de padrão de engenharia (evals de IA, observabilidade e os que vierem) vivem em `docs/padroes/` e são consultados na mesa de Desenho quando a fatia toca o tema. O plano registra os cartões aplicados.

## Gestão de trabalho

- O backlog macro é o `docs/roadmap.md`: a ordem oficial das fatias.
- O backlog granular vive no GitHub Issues deste repositório, com label de prioridade: `P0` fura a fila do roadmap, `P1` entra na próxima janela, `P2` espera agrupamento. Milestones podem mapear fatias futuras.
- Issue não vira código, issue vira fatia. Quando promovida, entra na mesa de Intenção e nasce uma spec. A issue referencia a spec e fecha quando a fatia sobe.
- Não existe `backlog.md`. Backlog é consultado sob demanda via `gh issue list`, filtrado por label. Ele não entra no contexto das sessões.

## Engenharia de contexto e harness

Estouro de contexto causa alucinação. Estas regras protegem toda sessão de trabalho:

1. Este `CLAUDE.md` tem teto de 120 linhas. Ele é índice e regra dura: aponta para `docs/`, não inlina conteúdo.
2. Contexto mínimo com recuperação sob demanda. Cada agente lê só o que o mandato pede: a constituição e a spec da fatia atual. Carregar spec de outra fatia, dump de arquivo inteiro ou backlog completo é violação.
3. Estado vive em artefato, não em conversa. O disco é a memória, a sessão é descartável. Estado durável vive em arquivo: `04-tasks.md`, registro de decisão da mesa, nota em `docs/decisoes/`. Sessão nova retoma do arquivo, não da conversa. Prefira sessão nova por fase.
4. Subagente lê, sessão principal decide. Leitura pesada vai pra subagente, que devolve síntese. Mesa com teto: máximo duas rodadas de crítica cruzada e registro de decisão curto.

## Stack padrão

Decisão tomada para reduzir superfície e aproveitar o que já existe. Mudar qualquer item da stack ou da topologia exige nota de decisão registrada em `docs/decisoes/`.

- Linguagem: [[LACUNA:stack-linguagem | pergunta: qual a linguagem principal do projeto | ex.: TypeScript em todo o projeto]]
- Backend: [[LACUNA:stack-backend | pergunta: qual backend e banco o projeto usa | ex.: Supabase com Postgres, Auth, Storage e Row Level Security]]
- Web: [[LACUNA:stack-web | pergunta: qual o framework web e a postura de entrega | ex.: Next.js com App Router, web-first com PWA]]
- Mobile: [[LACUNA:stack-mobile | pergunta: o projeto tem mobile e com qual tecnologia | ex.: Expo (React Native) quando o roadmap pedir; não ter mobile vale]]
- Integrações: [[LACUNA:stack-integracoes | pergunta: quais integrações externas e serviços alugados | ex.: pagamento e e-mail como serviço]]
- Design system: [[LACUNA:design-system | pergunta: o projeto tem design system definido e qual é, apontando onde ele vive | ex.: tokens e CSS no repositório acme-designsystem; não ter vale]]

## Topologia de execução

- Dado: [[LACUNA:topologia-dado | pergunta: onde o dado vive e em qual região | ex.: Postgres gerenciado na região de São Paulo, dado de brasileiro em solo brasileiro sob a LGPD]]
- Aplicação: [[LACUNA:topologia-aplicacao | pergunta: onde e como a aplicação roda | ex.: um host com containers, proxy reverso com TLS, camada de app sem estado]]
- Pipeline: [[LACUNA:topologia-pipeline | pergunta: como o build e o deploy acontecem | ex.: CI monta a imagem e publica no registry, o host faz pull; migration versionada e reversível; segredo em ambiente]]

## Regras de domínio e privacidade

- Toda tabela com dado pessoal usa Row Level Security no Supabase. Sem exceção.
- Cada usuário só enxerga o próprio dado. Os demais papéis enxergam conforme função.
- Papéis mínimos: [[LACUNA:papeis-projeto | pergunta: quais os papéis de acesso do projeto | ex.: usuario, equipe, admin]]
- Nenhum dado pessoal vai pra log, telemetria ou mensagem de erro.
- Toda coleta de dado precisa de base legal clara (LGPD). Em caso de dúvida, o agente `grc-reviewer` decide e registra.
- Compliance específico: [[LACUNA:compliance-especifico | pergunta: além da LGPD, quais frameworks se aplicam, entre NIST CSF 2.0, NIST AI RMF, ISO 42001, ISO 27001, GDPR, EU AI Act, SOC 2, CIS Controls, COBIT e ITIL; nenhum vale | ex.: ISO 27001 e SOC 2]]
- Integrações externas guardam segredo em variável de ambiente, nunca no código.
- [[LACUNA:dado-sensivel-dominio | pergunta: qual dado do domínio é sensível e portanto risco alto por padrão | ex.: dado de saúde, avaliação de desempenho, dado de menor]]

## Convenções de código

- Nomes de arquivo e pasta em kebab-case; componentes React em PascalCase.
- Sem comentário óbvio. Comentário explica porquê, não o quê.
- Migration de banco sempre versionada e reversível.
- Toda função de acesso a dado assume que o RLS está ligado e testa isso.

## O que nunca fazer

- Nunca começar uma fatia sem spec aprovada em `specs/`.
- Nunca abrir leitura de dado pessoal sem política de acesso.
- Nunca colocar segredo no repositório.
- Nunca pular o `grc-reviewer` em fatia que toca dado pessoal.
- Nunca expor dado pessoal a agente via MCP sem token escopado e política de acesso idêntica.
- Nunca trazer Kubernetes ou self-host de Supabase sem nota de decisão registrada em `docs/decisoes/`.
- Nunca deixar uma fase fechar engolindo um veto. Veto sobrevive ao consenso.
- Nunca manter backlog em markdown no repo. Backlog é issue no GitHub, consultada sob demanda.
- Nunca deixar esta constituição passar de 120 linhas. Conteúdo novo vai pra `docs/` e é referenciado.
- Nunca ligar plugin de memória automática sem nota de decisão. A memória do projeto é curada e vive em disco.
- Nunca expor superfície MCP sem autenticação explícita e rate limiting por identidade.
- [[LACUNA:nunca-do-dominio | pergunta: quais os nunca específicos do domínio | ex.: nunca construir o que se aluga]]

## Estilo de escrita (vale para qualquer texto gerado)

[[LACUNA:referencia-estilo | pergunta: qual o estilo de escrita de todo texto gerado no projeto | ex.: voz ativa, frase curta, sujeito explícito, sem travessão longo em prosa, sem frase-muleta de IA]] Isso vale para README, mensagens de commit, textos de interface e qualquer copy do produto.
