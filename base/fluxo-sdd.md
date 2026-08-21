# O fluxo SDD da ITXPRO

> Documento canônico do fluxo. A versão resumida vive na constituição de cada projeto. Este detalha a mecânica.

A spec é a fonte da intenção, o código é consequência dela. Cada fatia do produto passa por três fases. Cada fase é uma mesa redonda onde as vozes relevantes discutem, convergem e emitem uma decisão unificada. A regra de ouro: uma fatia por vez. Nada começa antes da anterior estar no ar.

## As três fases

### Fase 1 — Intenção

Mesa: spec-writer (conduz), security-privacy-architect, ux-architect.

Discussão: o spec-writer traz o quê e por quê. A segurança classifica o risco e nomeia o que está em jogo de privacidade. O UX nomeia a barra de experiência. Ninguém decide técnica aqui.

Insumo visual: referência visual do dono entra na mesa como imagem, desktop e mobile, gravada em `specs/NNN-*/insumos/`; referência que virou só texto é lacuna. A mecânica de captura e a regra de persistência vivem na skill do condutor.

Saída: uma spec só, que já carrega problema, jornada, critérios de aceite, classificação de risco, intenção de experiência, postura AI-first, exposição a agente, desvios da referência e questões abertas.

Portão: humano, sempre. Você lê a spec, responde as questões e aprova. O condutor apresenta a seção "Desvios da referência" item a item, ao lado das divergências e das questões abertas; desvio sem a sua resposta é lacuna, não convergência, e bloqueia o portão. Convergência da mesa que contraria a referência ou o seu pedido não se veste de decisão: sobe ao portão, sempre.

### Fase 2 — Desenho

Mesa: architect (conduz), security-privacy-architect, ux-architect, devsecops.

Discussão: o architect propõe o desenho. A segurança molda o controle de acesso e a ameaça ao vivo. O UX molda interação e aplica o sistema de design. O DevSecOps molda deploy, config, observabilidade e orçamento de desempenho. Tudo tecido junto, não anexado depois.

Saída: um plano e uma lista de tarefas, com modelo de dados e política de acesso, fronteiras e módulos declarados, modelagem de ameaça proporcional, contratos prontos pra agente, design de interação, plano de deploy e config, e budget de desempenho.

Portão: por exceção, com três gatilhos nomeados. O desenho passa sozinho quando a mesa fecha sem divergência, sem veto e sem estouro do teto da classe. Ele sobe pro humano quando há divergência aberta, veto de segurança ou estouro de teto (reclassificação da classe para cima conta como estouro). Quando o portão de Intenção emitiu a pré-autorização (frase-modelo dita pelo condutor e aprovada pelo dono; o texto literal e os campos de rastro vivem na skill do condutor), o Desenho fechado sem nenhum gatilho é publicado pelo condutor, que declara isso em uma linha; qualquer gatilho anula a pré-autorização, que não renasce, e o portão sobe nomeando-o. Nos primeiros slices de um projeto, dá pra manter portão fixo até confiar na mesa, e depois soltar para a exceção.

### Fase 3 — Construção e veredito

Construção: cada implementer constrói uma tarefa por vez; a regra vale por implementer, não por fatia. A marcação de independência das tarefas no plano é declarativa e dormente: execução paralela de implementers aguarda decisão própria do framework.

Mesa de veredito: reviewer (conduz), grc-reviewer (veto), ux-architect, devsecops, e security-privacy-architect conforme o risco.

Saída: um veredito único, aprovado ou reprovado, com os bloqueantes consolidados. O veto do grc-reviewer sobrevive ao consenso.

Portão: humano, sempre. Você vê um parecer, decide o merge.

Resultado: dois portões fixos seus (Intenção e Veredito) e um por exceção (Desenho). Três paradas no pior caso, duas no caso comum.

## O condutor

O pipeline tem um dono operacional: o condutor, que é a sessão principal do Claude Code, não um nono subagente. Subagente roda isolado e não conversa com o usuário; ele não pode segurar portão humano nem ser ponto de contato com o dono do projeto.

O mandato do condutor:
- Identificar em que fase a fatia está e convocar a mesa certa, com o mandato de cada voz.
- Sintetizar os produtos da mesa: o artefato unificado e o registro de decisão curto.
- Parar nos portões humanos e apresentar ao dono do projeto a decisão, as divergências e o que precisa de resposta.
- Nunca implementar nem julgar. Quem constrói é o implementer, quem julga é a mesa de Veredito.
- Manter o estado do pipeline em disco (`specs/NNN-*/`), nunca na conversa. Sessão nova de condução retoma do disco.
- Fechar a fase publicando: estado em disco é o branch padrão do repositório publicado em `origin`; o condutor integra por fast-forward e publica antes de recomendar sessão nova, dentro dos limites declarados na skill. Vale também para o Desenho fechado por exceção sob pré-autorização da Intenção, com o rastro declarado em uma linha; o mecanismo e o literal vivem na skill.

A skill `sdd-conductor` carrega esse mandato como comando invocável em qualquer projeto e chega com o plugin (`skills/sdd-conductor/`).

## Como a mesa funciona

No Claude Code os subagents não conversam sozinhos. A sessão principal conduz a mesa. Ela convoca cada especialista com seu mandato, roda uma ou duas rodadas de crítica cruzada onde cada voz vê a posição das outras e responde da sua ótica, e sintetiza dois produtos: o artefato unificado (spec, plano ou veredito) e um registro de decisão curto, que diz o que convergiu, o que divergiu e o que precisa do humano. Cada voz é instruída a criticar da sua ótica antes de fechar. Sem isso, vozes separadas viram consenso morno e perdem a razão de existir. A mesa pode virar um Workflow quando valer a pena o determinismo.

## Proporcionalidade

A cerimônia escala com quatro triagens feitas no começo:

- Risco de dado (segurança). Baixo risco passa leve. Fatia que toca dado pessoal sensível dispara o pacote completo: modelagem de ameaça (STRIDE e LINDDUN), classificação e análise de risco.
- Superfície de tela (UX), em três níveis. Sem UI: o ux-architect sai da mesa. UI simples (CRUD, form interno, dashboard operacional): barra visual de uma linha + DS, sem moodboard. Superfície rica: Barra visual completa na spec, moodboard obrigatório na mesa de Desenho, veredito visual lado a lado. É rica quando o dono deu referência visual OU a página é pública e carrega a marca. Referência do dono a artefato visual (site, documento, relatório, apresentação) sempre convoca o ux-architect na mesa de Intenção.
- Exposição a agente (AX). Fatia que expõe MCP convoca o agent-experience-architect e faz a segurança co-desenhar a superfície. Fatia que não expõe fica só com o princípio AI-first nos contratos.
- Tamanho da entrega (classe de fatia). A triagem atribui a classe: leve, média ou plena. A classe entra no registro de Intenção na linha `Classe: X, assinada por security`, assinada pela voz de segurança. Registro de Intenção sem essa linha bloqueia a convocação da mesa de Desenho. Reclassificação para baixo depois do desenho sobe ao portão; ninguém rebaixa classe para caber no teto.

### Classe de fatia e teto de tarefas

Cada classe carrega um teto de tarefas do plano: leve até 10, média até 20, plena sem teto fixo e com justificativa por excedente registrada no plano. Os números são default do framework; a constituição do projeto pode recalibrá-los, com registro. Invariante de granularidade: cada tarefa tem um único critério de pronto verificável, e tarefa composta conta pelo número de critérios; fundir tarefas para caber no teto é estouro disfarçado. Estouro de teto sobe sempre ao dono, no portão de Desenho, mesmo com a mesa fechada sem bloqueio; não há margem delegada à mesa. Reclassificação da classe para cima durante o Desenho conta como estouro.

### Piso por classe

O teto corta cerimônia, nunca piso. O piso de segurança de cada classe vive aqui, casa única: templates, agentes e skills apontam para esta seção, não a copiam. Colisão entre piso e teto não se resolve pela aritmética: é estouro e sobe ao dono.

- Piso universal (toda classe, toda fatia com código): fundação presente e verificada com versão; nenhum segredo em código, log ou artefato (gitleaks ativo); nenhum dado pessoal em log, telemetria ou mensagem de erro.
- Leve: piso universal. Leve com página pública NUNCA dispensa headers de segurança e CSP herdados da fundação, verificados e não presumidos. Leve que toca dado pessoal nunca dispensa política de acesso por papel na tabela ou endpoint tocado.
- Média: tudo da leve + validação de entrada em todo endpoint novo + política de acesso nasce junto com a tabela, nunca em tarefa separada cortável.
- Plena: tudo da média + modelagem de ameaça conforme o risco de dado (STRIDE/LINDDUN quando sensível) + security obrigatório no Veredito.

## Os portões e o veto

- Dois portões humanos fixos: aprovação da spec (Intenção) e decisão de merge (Veredito).
- Um portão por exceção: o Desenho, com três gatilhos nomeados: divergência aberta, veto e estouro de teto (reclassificação da classe para cima conta como estouro). O estouro chega ao dono em mensagem de formato fixo, até cinco linhas, sem anexar o plano; o modelo literal vive na skill do condutor, e o normativo das classes e dos tetos vive na triagem de proporcionalidade, acima. O portão de Intenção pode pré-autorizar a publicação do Desenho fechado sem gatilho; a frase-modelo é casa única na skill do condutor, a anulação por gatilho é definitiva, e a constituição do projeto pode restringir esse mecanismo, nunca ampliar.
- O veto do grc-reviewer sobrevive ao consenso da mesa. Uma fase nunca fecha engolindo um veto.
- Segregação de função: o security-privacy-architect desenha a restrição no começo, o grc-reviewer julga o resultado no fim. Um não substitui o outro.

## Engenharia de contexto nas mesas

A mesa gasta token e contexto, e os dois têm teto:

- Máximo duas rodadas de crítica cruzada. Mandato afiado entra, decisão unificada sai.
- Cada voz recebe só o que o mandato pede: a constituição, a spec da fatia atual e o mapa do sistema, quando existir. Nada de spec antiga, backlog ou dump de arquivo.
- Leitura pesada (varrer código, auditar, pesquisar) vai pra subagente, que devolve síntese. O dump morre no contexto do subagente.
- O produto da mesa vive em disco: o artefato (spec, plano ou veredito) e um registro de decisão curto. Sessão nova retoma do arquivo, não da conversa. "Estado em disco" significa branch padrão do repositório publicado no remoto: commit só em branch de trabalho é memória da sessão. Prefira sessão nova por fase.
- Nenhuma mesa fecha citando arquivo que ninguém abriu. Afirmação sobre o repo se verifica com ferramenta, não de memória.

O trabalho que alimenta as mesas vem do GitHub Issues (`P0`, `P1`, `P2`) e do `docs/roadmap.md`. Issue promovida entra na mesa de Intenção e vira fatia. Detalhe na nota de decisão de origem do framework.

## Padrões nomeados

O framework implementa padrões conhecidos da engenharia de agentes. Os nomes alinham o vocabulário com o mercado e tornam o framework ensinável:

- Plan-and-Execute no macro. O fluxo spec, plano, execução com portões humanos. Escolhido sobre ReAct puro no nível de fatia: planejar uma vez e executar tarefas pequenas gasta menos token e alucina menos do que re-raciocinar a cada passo.
- ReAct no micro. Cada agente, dentro da sua tarefa, opera no loop raciocínio-ação-observação do Claude Code.
- Blackboard como contexto compartilhado. Os agentes não conversam entre si; colaboram por um quadro comum, os artefatos da fatia em disco (spec, plano, tarefas, threat-model). A mesa é a leitura cruzada desse quadro. O mapa do sistema estende o quadro na dimensão entre fatias: memória estrutural curada que toda fatia mantém.
- Taxonomia de memória. Semântica: a constituição, o que é sempre verdade. De trabalho: os artefatos da fatia atual. Episódica: `docs/decisoes/` e o registro de conhecimento do projeto, o que aconteceu e por quê. Os agentes são deliberadamente reativos e sem estado; a memória vive em disco, curada. Memória automática (captura de transcript) não entra sem nota de decisão.

## Governança de contribuição

A contribuição ao framework passa por revisão de PR no repositório canônico, com varredura de acoplamento e registro de decisão. Essa governança é interna e vive no repositório canônico, em documento próprio, fora do pacote distribuído.
