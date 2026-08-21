# Cartão de padrão — Fundação: proteção de segredo (gitleaks)

> Herdado no setup; vale para toda fatia com código. A configuração vive nos arquivos herdados, nunca duplicada aqui.
> Versão: 1.0 · Revisado: 2026-08-20 · Gatilho de revisão: release do plugin · Dono: security-privacy-architect

## Contexto

A proteção de segredo do projeto já vem montada no setup, em três camadas. Este cartão nomeia as camadas e a regra de mudança, para que nenhuma fatia recrie varredura nem bifurque a config.

## Nosso padrão

- Três camadas herdadas: (1) hook local que bloqueia `git commit` com segredo na sessão do agente, fail-closed; (2) workflow de CI que varre o repositório (`.github/workflows/gitleaks.yml`); (3) required check no branch padrão, quando o plano do GitHub permite, configurado pela pessoa.
- A config é uma só, a herdada: `.gitleaks.toml` na raiz do projeto. Nenhuma fatia cria config paralela.
- Mudança de allowlist entra por PR revisado, com justificativa; allowlist sem âncora de caminho ou mais ampla que o necessário é reprovável.
- Piso universal do fluxo: nenhum segredo em código, log ou artefato, com a varredura ativa.

## Proibido

- Duplicar ou bifurcar a config herdada.
- Allowlist por commit direto, sem PR.
- Desligar o hook ou o workflow para destravar um commit: segredo achado se remove e se revoga, não se allowlista às pressas.

## Exige nota de decisão

- Regra nova de detecção específica do domínio.

## Como verificar herança

- Arquivo: `.gitleaks.toml` na raiz e `.github/workflows/gitleaks.yml`.
- Comando: `gitleaks dir . --config .gitleaks.toml --no-banner --exit-code 1` termina sem achado.
