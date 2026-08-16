# Pinagem do hookify

O plugin hookify não tem campo de versão no `plugin.json` (o cache registra literalmente `unknown`): pinagem por semver é impossível hoje (lacuna declarada no plano da fatia 001). Enquanto isso, a pinagem tem duas camadas: este registro por hash, e a suíte de simulação que roda no CI do repositório canônico como tripwire — com os limites nomeados nas lacunas declaradas do conjunto de hooks, no repositório canônico.

## Registro (2026-08-15)

| Campo | Valor |
|---|---|
| Plugin | `hookify@claude-plugins-official` (autor: Anthropic) |
| Versão declarada pelo plugin | `unknown` (sem campo de versão no `plugin.json`) |
| Manifest de instalação | `~/.claude/plugins/.install-manifests/hookify@claude-plugins-official.json` |
| SHA-256 do manifest | `bbd81cf39a73f3b79e2cfd7c855a091dac64da243fd967ac66ff97b8b2f7bbf0` |
| Instalado em | 2026-08-07T18:33:58Z |
| Marketplace | `anthropics/claude-plugins-official` (GitHub) |
| Snapshot local do marketplace | 2026-08-07T19:38:35Z (`known_marketplaces.json`, campo `lastUpdated`) |
| Commit do marketplace | `82a73a367be4991ff22e2b43317b3956933c9f9a` (2026-08-07T18:18:30Z) |

O manifest de instalação lista o SHA-256 de cada arquivo do plugin (motor `core/rule_engine.py`, `core/config_loader.py`, hooks de evento, skill `writing-rules`): o hash do manifest pina o conjunto inteiro.

**Como o commit foi resolvido (caveat honesto):** a cópia local do marketplace não é um checkout git; o commit acima é o último de `anthropics/claude-plugins-official` anterior ao snapshot local, resolvido via `gh api` pela data. Verificação cruzada feita em 2026-08-15: o `plugin.json` do hookify nesse commit tem SHA-256 `926ed28095535263e3953ac30a3be8c034ff8e3efd1ce28c529cf6e0ba8e902b`, idêntico ao registrado no manifest local.

## Regra de reavaliação

Quando o plugin ganhar campo de versão, esta pinagem é reavaliada: o registro passa a pinar por semver, este arquivo registra a versão adotada e a mudança entra via nota de decisão em `docs/decisoes/`, como toda mudança de regra de enforcement. Até lá, atualização do hookify na máquina exige: recalcular o hash do manifest, atualizar esta tabela no mesmo commit e rodar a suíte de simulação antes de confiar nas regras.
