# Cartão de padrão — Fundação: proteção de segredo (gitleaks)

> Herdado no setup; vale para toda fatia com código. A configuração vive nos arquivos herdados, nunca duplicada aqui.
> Versão: 1.1 · Revisado: 2026-09-04 · Gatilho de revisão: release do plugin · Dono: security-privacy-architect

## Contexto

A proteção de segredo do projeto já vem montada no setup, em três camadas. Este cartão nomeia as camadas e a regra de mudança, para que nenhuma fatia recrie varredura nem bifurque a config. A v1.1 fecha dois buracos: o gate local passa a varrer o índice também no `--continue` de merge, rebase e cherry-pick, e o CI passa a ler o merge commit e a árvore do resultado, além do histórico.

## Nosso padrão

- Três camadas herdadas:
  - (1) Hook local, na sessão do agente, que bloqueia `git commit` e os três `--continue` (`git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`) com segredo no índice. Fail-closed: se a varredura não conclui, o comando não passa.
  - (2) Workflow de CI (`.github/workflows/gitleaks.yml`) com dois passos no mesmo job `gitleaks` e um check só, `--redact` nos dois, sem `continue-on-error`. Histórico: `gitleaks git . --log-opts="--full-history --all --diff-filter=tuxdb -m"`. Resultado: `gitleaks dir .`, com caminho `.` a partir da raiz, para a allowlist ancorada casar. Passo novo entra nesse job, nunca em job novo: a proteção de branch referencia o check pelo nome.
  - (3) Required check no branch padrão, quando o plano do GitHub permite, configurado pela pessoa.
- Por que o valor composto em `--log-opts`: a opção substitui o comando default do binário, não acrescenta. `-m` sozinho perde `--all` e deixa de ler ref fora da ancestralidade do HEAD. O valor repete o default inteiro (`--full-history --all --diff-filter=tuxdb`) e soma `-m`, que mostra o merge commit como diff contra cada pai: assim aparece o segredo nascido na resolução de conflito e removido no commit seguinte. Com `-m`, achado em merge commit sai uma vez por pai, com o mesmo fingerprint: duas linhas são um segredo, não dois.
- Feche conflito por qualquer dos quatro caminhos (`git commit` ou `--continue`): o gate local varre o índice nos quatro. Código de ramo paralelo entra por PR, obrigatório; o CI é autoritativo onde a proteção de branch exige o check e sinal onde não exige.
- Limite: `git revert --continue` e `git am --continue` ficam fora do gate (issue #62); nesses caminhos, só o CI alcança.
- A config é uma só, a herdada: `.gitleaks.toml` na raiz do projeto. Nenhuma fatia cria config paralela.
- Mudança de allowlist entra por PR revisado, com justificativa e path exato; allowlist sem âncora de caminho ou mais ampla que o necessário é reprovável.
- Piso universal do fluxo: nenhum segredo em código, log ou artefato, com a varredura ativa.

## Proibido

- Duplicar ou bifurcar a config herdada. `.gitleaksignore` está fora do padrão: falso positivo entra por path exato no `.gitleaks.toml`, via PR.
- Calar achado por diretório inteiro ou por regex na allowlist.
- Allowlist por commit direto, sem PR.
- Passo de varredura com `continue-on-error` ou em job separado do check `gitleaks`.
- Desligar o hook ou o workflow para destravar um commit ou um `--continue`: segredo achado se remove e se revoga, não se allowlista às pressas.

## Exige nota de decisão

- Regra nova de detecção específica do domínio.

## Como verificar herança

- Arquivo: `.gitleaks.toml` na raiz e `.github/workflows/gitleaks.yml`.
- Comando: `gitleaks dir . --config .gitleaks.toml --redact --no-banner --exit-code 1` termina sem achado em checkout limpo (clone novo, `git archive HEAD` extraído ou o próprio CI). Em checkout de trabalho, worktrees ligados criados sob a raiz, o diretório de staging do empacote e qualquer artefato sob a raiz contam: `dir` lê ignorado e não rastreado, e a allowlist ancorada não os cala, de propósito. Achado ali se investiga; nunca se allowlista diretório para calar. O critério de herança é o checkout limpo: vermelho só no checkout de trabalho aponta o que está no disco, não o que o repositório rastreia.
- Comando: `gitleaks git . --config .gitleaks.toml --redact --no-banner --exit-code 1 --log-opts="--full-history --all --diff-filter=tuxdb -m"` termina sem achado em clone com histórico completo (o CI faz checkout com `fetch-depth: 0`). Árvore extraída de `git archive` não serve aqui: não carrega `.git`.
