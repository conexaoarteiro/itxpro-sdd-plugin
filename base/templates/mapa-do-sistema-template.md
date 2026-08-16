# Mapa do sistema — [Nome do projeto]

> Vive em: `specs/_arquitetura/mapa-do-sistema.md`
> Teto: 120 linhas. Artefato interno do projeto.

Este mapa nasce na primeira fatia com código: o architect declara as entradas iniciais na seção "Fronteiras e módulos" do plano, o implementer materializa o arquivo a partir deste seed e o reviewer confere no Veredito. O mapa só muda pelo pipeline da fatia. Edição avulsa é desvio.

## O que nunca entra aqui

Segredo, credencial, URL interna com token, dado pessoal e detalhe de infra além da fronteira do módulo. Se uma entrada parece precisar disso, descreva a fronteira, não o acesso.

## Regras de estrutura

- Módulo nasce por domínio da fatia vertical, não por camada técnica.
- `shared` exige dois usos reais. Antes disso, o código vive no módulo que o usa.
- Padrão clássico entra quando o desenho pedir, não por antecipação.

## Módulos

Uma entrada por módulo. Nome em kebab-case como heading, três campos fixos.

### [nome-do-modulo]

- Propósito: [o que o módulo resolve, em uma frase]
- Expõe: [contratos, funções ou rotas que outros módulos usam]
- Consome: [módulos ou serviços de que depende]
