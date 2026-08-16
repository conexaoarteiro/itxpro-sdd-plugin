# Changelog — itxpro-sdd

Régua de versão, pela ótica do contrato que o agente adotante lê: major quebra nome, caminho ou instrução existente; minor adiciona sem quebrar; patch corrige texto.

## 0.1.0 — 2026-08-15

Classificação: minor (primeira versão distribuída; tudo é adição, nada quebra).

Entrega:

- Comando `/sdd`, despachante único do pipeline.
- Skill `sdd-setup`: entrevista em seis blocos, preenchimento da constituição por lacuna com id, registro append-only da entrevista, esqueleto por cópia.
- Skill `sdd-conductor` e os nove agentes das mesas.
- Hooks de enforcement via `hooks.json`: gate de segredo em commit (fail-closed), aviso de implementação sem spec aprovada, teto de 120 linhas da constituição. Regras hookify no payload de setup.
- Payload `base/`: constituição-template com sintaxe de lacuna, templates numerados 01 a 06, fluxo SDD, diagrama do pipeline, `.gitleaks.toml` e workflow de CI do gitleaks.

Integridade: sha256:051e6958611b8c8322b8ce91ab4bb2ee02e6f6f52058419f9cf66ce176114292 (amarração 0.1.0 → hash; conjunto do pacote, excluindo CHANGELOG.md e INTEGRIDADE.txt).
