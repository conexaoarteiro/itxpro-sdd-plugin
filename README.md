# itxpro-sdd

Framework de Spec-Driven Development da ITXPRO como plugin do Claude Code. A spec é a fonte da intenção, o código é consequência: cada fatia passa por mesas de Intenção, Desenho e Veredito, com portões humanos e veto que sobrevive ao consenso.

## Instalação

```
/plugin marketplace add conexaoarteiro/itxpro-sdd-plugin
/plugin install itxpro-sdd@itxpro-sdd-plugin
```

Instale sempre pinado em tag (`vX.Y.Z`), nunca em branch. Acesso: repositório privado da ITXPRO.

## Pré-requisito: gitleaks

O gate de segredo em commit é fail-closed: sem gitleaks (>= 8.21.0) no PATH, commit nenhum passa. A instalação do gitleaks é sua, executada por você: o plugin imprime o comando e recomenda verificar o checksum do binário contra o release oficial. Nenhum agente executa esse download.

## O que o plugin disponibiliza

- Comando `/sdd`: o ponto de entrada único. Detecta o estado do projeto e despacha.
- Skill `sdd-setup`: entrevista em seis blocos (~15 minutos) que preenche a constituição do seu projeto e instancia o esqueleto. "Não sei" vale e vira pendência declarada.
- Skill `sdd-conductor`: o condutor do pipeline de fatias.
- Nove agentes: as vozes das mesas (spec-writer, architect, security-privacy-architect, ux-architect, devsecops, implementer, reviewer, grc-reviewer com veto, agent-experience-architect engatilhado).
- Hooks de enforcement: gate de segredo em commit, aviso de implementação sem spec aprovada, teto de 120 linhas da constituição, mais as regras hookify no payload de setup.
- Payload `base/`: constituição-template com lacunas, templates numerados dos artefatos (01 a 06), fluxo SDD, diagrama do pipeline e configuração do gitleaks.

## Depois de instalar

Rode `/sdd`. Sem constituição no projeto, ele aponta o setup; com constituição fechada, ele conduz a fatia.

## Local-only

Nada sai da sua máquina. O plugin não tem telemetria, não faz chamada de rede em arquivo executável e as respostas da entrevista só vivem em arquivos do seu repositório.
