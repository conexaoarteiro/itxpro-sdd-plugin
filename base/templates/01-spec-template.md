# Spec — [Nome da fatia]

> Status: rascunho | em revisão | aprovada
> Autor: mesa de Intenção (spec-writer, security-privacy-architect, ux-architect)
> Data:

## Problema

Que dor real isso resolve? Pra quem?

## Usuário e papel

Quem usa esta fatia e em que papel (conforme os papéis definidos na constituição do projeto).

## Jornada principal

O caminho feliz, passo a passo, do ponto de vista do usuário. Sem detalhe técnico.

## Critérios de aceite

Lista de afirmações verificáveis. Cada uma é testável.

- [ ] ...
- [ ] ...

## Classificação de risco

(security-privacy-architect) Que dado pessoal esta fatia toca, de quem, e com que base legal. Risco: baixo, médio ou alto. Dado pessoal sensível definido na constituição é sempre alto.

## Intenção de experiência

(ux-architect) A barra de experiência desta fatia. O que faz o usuário entender onde está em poucos segundos. A superfície de tela: rica, simples ou sem UI.

**Barra visual** (obrigatória em superfície rica; é rica quando o dono deu referência visual OU a página é pública e carrega a marca):

1. O que a página transmite em cinco segundos. Substantivo concreto; adjetivo genérico ("moderno", "clean", "profissional") é proibido.
2. Ativos visuais da referência que se preservam. Lista nominal (ex.: "hero com foto de pessoa real", "grade de 3 cards com ícone").
3. Anti-exemplo: a descrição de uma página que reprova no Veredito (ex.: "parede de texto centrado sobre fundo branco, sem imagem, botões default").

UI simples: barra visual de uma linha + DS, sem moodboard. Sem UI: a seção declara "sem UI" e o ux-architect sai da mesa.

## Exposição a agente

(AI-first) Esta fatia expõe alguma superfície MCP para os agentes dos usuários? Se sim, o security-privacy-architect co-desenha o acesso e o agent-experience-architect é convocado. Se não, os contratos só nascem prontos para agente, como manda o princípio.

## Desvios da referência

Quando o dono apontou referência ou insumo (site, fluxo, artefato, produto existente), na abertura da fatia ou durante a mesa, liste aqui cada desvio com três campos: o que a referência faz, o que a spec propõe, por quê. Cada item recebe status no portão de Intenção: respondido pelo dono ou lacuna. Convergência da mesa que contraria a referência ou o pedido do dono não é decisão: sobe ao portão. Sem referência, o texto obrigatório desta seção é "sem referência declarada".

## Fora de escopo

O que esta fatia explicitamente NÃO faz.

## Questões abertas

O que precisa de resposta humana antes de planejar.
