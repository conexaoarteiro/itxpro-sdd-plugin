# Plano Técnico — [Nome da fatia]

> Status: rascunho | aprovado
> Autor: mesa de Desenho (architect, security-privacy-architect, ux-architect, devsecops)
> Baseado em: 01-spec.md

## Abordagem

Resumo da solução técnica em poucos parágrafos. A mais simples que atende a spec.

## Fronteiras e módulos

(architect) O módulo que a fatia cria ou estende, o que ele expõe e o que consome. A atualização correspondente de `specs/_arquitetura/mapa-do-sistema.md` entra como tarefa da fatia. Na primeira fatia com código, esta seção declara as entradas iniciais do mapa. Se a fatia não toca módulo, diga.

## Modelo de dados

Tabelas, colunas, relações. Para cada tabela com dado pessoal, a política de acesso por papel (RLS quando a stack for Supabase).

## Contratos

Telas, endpoints e a forma dos dados que trafegam.

## Integrações externas

O que entra, o que sai, e as variáveis de ambiente necessárias.

## Modelagem de ameaça

(security-privacy-architect, proporcional ao risco) Para risco alto, STRIDE para segurança e LINDDUN para privacidade. Ameaça, vetor e mitigação. Requisitos de controle de acesso por papel. O que não vai para log nem erro.

## Experiência e sistema de design

(ux-architect) Fluxo de telas e estados (carregando, vazio, erro, sucesso). Micro-interação e transição. Componentes do sistema de design aplicados. Meta de performance percebida.

**Moodboard de uma página** (obrigatório em superfície rica). A imagem do moodboard vive em `specs/NNN-*/evidencias/` e é citada aqui por link relativo. Conteúdo mínimo:

1. Imagem: no mínimo o screenshot anotado da referência (desktop e mobile quando houver).
2. Paleta aplicada: quais tokens do DS carregam a atmosfera desta página, nomeados.
3. Tipografia em uso: escala e peso por nível de hierarquia da página.
4. Composição: esqueleto da página (ordem, proporção e densidade das seções).
5. Imagem própria: o que a página mostra (assunto, enquadramento) e o orçamento (formato, peso, alvo de LCP).
6. Lista do que reprova: os anti-exemplos herdados da Barra visual da spec.

Cada linha é uma decisão que o implementer pode violar. Sem imagem, não é moodboard.

**Orçamento de imagem de hero**: alvo de LCP mantido, formato e peso declarados. Veto de imagem por performance sem orçamento apresentado é inválido.

## Deploy, configuração e observabilidade

(devsecops) Como a fatia faz deploy e rollback. O que muda em ambiente, segredo e migration. Observabilidade. Confirmação de que o app segue sem estado.

## Orçamento de desempenho

(architect com devsecops) Budget explícito: p95 de latência dos pontos críticos, Core Web Vitals alvo, e o plano de índice das queries que a fatia adiciona.

## Contratos prontos para agente

(architect, princípio AI-first) Os contratos das telas e endpoints nascem consumíveis por agente: tool-shaped, com forma de dado clara e escopo por papel.

## Padrões aplicados

Cartões de `docs/padroes/` consultados nesta fatia e como se aplicam. Fatia com LLM em runtime consulta `evals-de-ia.md`. Fatia que vetoriza dado, envia dado a provider ou monta dataset consulta `dados-de-ia.md`. Fatia que sobe pra produção consulta `observabilidade.md`. Se nenhum cartão se aplica, diga.

## Riscos técnicos

O que pode dar errado e o plano pra cada um.

## Decisões pro registro do projeto

O que merece virar nota de decisão em `docs/decisoes/`.
