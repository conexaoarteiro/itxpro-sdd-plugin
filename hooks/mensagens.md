# Catálogo de mensagens dos hooks

Fonte única do texto que cada hook exibe. As regras hookify copiam o texto daqui palavra por palavra (a mensagem hookify é markdown estático). Os scripts nativos (T04, T05, T06) usam o texto daqui e preenchem os campos entre chaves, como `{arquivo}` e `{linha}`, com valores estruturados, nunca com saída bruta de ferramenta. Zero saída sem mensagem deste catálogo.

Anatomia fixa de toda mensagem: **fato → regra → caminho**. O fato diz o que foi detectado. A regra cita a seção da constituição que fundamenta. O caminho é ação executável, não conselho vago.

Âncoras verificadas em `base/constituicao-template.md` do pacote (título literal das seções): "O que nunca fazer", "Gestão de trabalho", "Regras de domínio e privacidade", "Engenharia de contexto e harness". Mensagem nova só entra citando seção que existe no template.

Vocabulário único nas três camadas de segredo (aviso na escrita, gate de commit, varredura no CI), que contam a mesma história com os mesmos termos: o segredo sai do código e vai pra variável de ambiente; a chave se documenta no `.env.example`, nunca o valor; falso positivo entra no `.gitleaks.toml` via PR (allowlist versionada, path exato); a varredura no CI é a linha autoritativa.

## 1. `backlog.md` proibido

Bloqueio. Regras hookify `block-backlog-md` (evento file, `hookify.block-backlog-md.local.md`) e `block-backlog-md-bash` (evento bash, `hookify.block-backlog-md-bash.local.md`, bloqueia `touch`, redireção `>`/`>>` e `cp`/`mv` com destino `backlog.md`). O critério da spec é "tentativa de criar `backlog.md` em qualquer diretório é bloqueada", então a via Bash tem a mesma regra e a mesma mensagem. Mensagem estática:

> Bloqueado: tentativa de escrever `backlog.md`. Backlog não vive em markdown neste repositório.
>
> Regra: constituição, seção "O que nunca fazer" ("Nunca manter backlog em markdown no repo") e seção "Gestão de trabalho".
>
> Caminho: registre a demanda como issue e consulte sob demanda:
>
> `gh issue create --title "resumo da demanda" --label P1`
>
> `gh issue list --label P0`

## 2. Segredo em escrita (shift-left)

Aviso. Regras hookify `warn-segredo-shift-left-file` e `warn-segredo-shift-left-bash`. São dois arquivos com o mesmo texto porque o motor hookify aceita um evento por regra e avalia condições em AND sobre o input da ferramenta: `content` não existe em input de Bash e `command` não existe em input de Write/Edit. A exclusão por path do corpus de teste do canônico está nas condições das duas regras, para o corpus de teste não disparar aviso. Restrição do parser do hookify, descoberta em execução real: o frontmatter não pode conter `---` literal (o parser corta ali e a regra quebra em silêncio), por isso o padrão PEM usa `-{5}` no lugar dos cinco hífens. Mensagem estática:

> Aviso (heurística): o texto contém um padrão que parece segredo (chave AWS `AKIA…`, token GitHub `ghp_…`, chave `sk-…` ou bloco PEM de chave privada). A detecção é regex simples, sem entropia e sem allowlist: pode ser falso positivo.
>
> Regra: constituição, seção "O que nunca fazer" ("Nunca colocar segredo no repositório") e seção "Regras de domínio e privacidade" (segredo em variável de ambiente, nunca no código).
>
> Caminho: o segredo sai do código e vai pra variável de ambiente; a chave se documenta no `.env.example`, nunca o valor. Falso positivo entra no `.gitleaks.toml` via PR (allowlist versionada, path exato). Esta é a camada de aviso na escrita: o gate de commit roda gitleaks e bloqueia; a varredura no CI é a linha autoritativa.

## 3. Segredo em commit (gate)

Bloqueio, fail-closed. Script `secret-commit-gate.py` (T04). Duas variantes.

Achado do gitleaks (o script preenche os campos com dados estruturados do report, valor sempre mascarado):

> Bloqueado: segredo detectado no commit. `{arquivo}:{linha}`, padrão {tipo}, valor `{valor_mascarado}`.
>
> Regra: constituição, seção "O que nunca fazer" ("Nunca colocar segredo no repositório").
>
> Caminho: o segredo sai do código e vai pra variável de ambiente; a chave se documenta no `.env.example`, nunca o valor. Depois, `git add` e repita o commit. Falso positivo entra no `.gitleaks.toml` via PR (allowlist versionada, path exato). A varredura no CI é a linha autoritativa: contornar este gate não passa do PR.

Fail-closed (gitleaks ausente do PATH ou erro de execução):

> Bloqueado: o gate de segredo não conseguiu rodar ({motivo}). O gate é fail-closed: sem varredura, nenhum commit passa.
>
> Regra: constituição, seção "O que nunca fazer" ("Nunca colocar segredo no repositório").
>
> Caminho: instale o gitleaks e repita o commit:
>
> `brew install gitleaks`
>
> Linux (binário oficial, ajuste versão e arquitetura):
>
> `curl -sSL https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz | tar -xz gitleaks && sudo mv gitleaks /usr/local/bin/`
>
> Versão mínima: README do plugin, seção "Pré-requisito: gitleaks".

Variante do CI (passo `if: failure()` do `gitleaks.yml` imprime no log do job, para a camada autoritativa falar a mesma língua; os achados, sempre com valor mascarado, ficam no passo anterior):

> Bloqueado: segredo detectado na varredura do CI. Os achados, com valor mascarado, estão no passo anterior deste job.
>
> Regra: constituição, seção "O que nunca fazer" ("Nunca colocar segredo no repositório").
>
> Caminho: o segredo sai do código e vai pra variável de ambiente; a chave se documenta no `.env.example`, nunca o valor. Falso positivo entra no `.gitleaks.toml` via PR (allowlist versionada, path exato). Esta varredura é a linha autoritativa: remova o segredo do histórico do branch e rotacione a credencial exposta.

## 4. Implementação sem spec aprovada

Aviso, fail-open. Script `spec-approval-warn.py` (T05):

> Aviso: escrita de código em `{arquivo}` sem nenhuma spec aprovada (nenhum `specs/*/01-spec.md` com a linha `Status: aprovada`).
>
> Regra: constituição, seção "O que nunca fazer" ("Nunca começar uma fatia sem spec aprovada em `specs/`").
>
> Caminho: leve a fatia à mesa de Intenção e aprove a spec no portão humano; a linha `Status: aprovada` no `01-spec.md` encerra o aviso. Este disparo ficou registrado em `.claude/hooks-log.jsonl` (regra, timestamp e path, nunca conteúdo).

## 5. Teto de 120 linhas do `CLAUDE.md`

Aviso, fail-open. Script `claude-md-limit-warn.py` (T06):

> Aviso: `CLAUDE.md` está com {n}/120 linhas.
>
> Regra: constituição, seção "Engenharia de contexto e harness" (item 1, teto de 120 linhas) e seção "O que nunca fazer" ("Nunca deixar esta constituição passar de 120 linhas").
>
> Caminho: mova o conteúdo novo para `docs/` e deixe no `CLAUDE.md` só a referência.
