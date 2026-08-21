# Cartão de padrão — Fundação: deploy e rollback

> Herdado no setup; consulte na mesa de Desenho de toda fatia que sobe para produção. O plano declara só o delta (migration, variável, job novo).
> Versão: 1.0 · Revisado: 2026-08-20 · Gatilho de revisão: release do plugin · Dono: devsecops

## Contexto

Deploy sem rollback testado é aposta. A fundação fixa o rito uma vez; fatia que redesenha deploy do zero está reconstruindo fundação, não entregando valor.

## Nosso padrão

- Rollback em um comando, testado: o rito de deploy declara o comando único de volta e o ensaia fora de produção antes da primeira subida real.
- Migration versionada e reversível, como manda a constituição; migration sem caminho de volta documentado não sobe.
- Camada de app sem estado: qualquer instância pode morrer e voltar sem perder dado; estado vive no banco e no storage gerenciados.
- Segredo em variável de ambiente do ambiente de deploy, nunca em arquivo do repo.
- Smoke após o deploy: uma verificação do fluxo principal, declarada no rito; falhou, rollback.

## Proibido

- Tarefa de fatia que recria o rito de deploy herdado; o plano declara o delta.
- Deploy manual fora do rito em produção.
- Migration irreversível sem escalada ao dono.

## Exige nota de decisão

- Mudar a topologia de deploy declarada na constituição.

## Como verificar herança

- Arquivo: o rito de deploy do projeto (workflow ou script) com o comando de rollback declarado.
- Comando: o comando de rollback declarado no rito, ensaiado em ambiente não produtivo, com o resultado citado no plano da primeira fatia que faz deploy.
