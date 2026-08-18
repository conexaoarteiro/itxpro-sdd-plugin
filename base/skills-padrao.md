# Skills padrão do framework SDD

> Herdado por todo projeto ITXPRO. Copie para `docs/skills-padrao.md` do projeto na adoção.
> Regra de precedência: a constituição define o processo, as skills são a mecânica de execução dentro das fases. Quando uma skill conflitar com a constituição, a constituição vence.

## Por fase e agente

| Agente | Skills padrão | Papel |
|---|---|---|
| condutor (sessão principal) | `sdd-conductor` (ITXPRO, `skills/sdd-conductor/` no plugin) | Conduz o pipeline, convoca as mesas, segura os portões |
| spec-writer | `superpowers:brainstorming` | Mesa de Intenção com hard gate: nada se constrói sem design aprovado |
| architect | `superpowers:writing-plans`, `supabase:supabase-postgres-best-practices`, `vercel:nextjs`, `context7` | Plano rigoroso em tarefas pequenas; boas práticas da stack; docs de biblioteca sob demanda em vez de memória do modelo |
| security-privacy-architect | `security-review`, `claude-security` (scan sob demanda) | Modelagem de ameaça com varredura real, proporcional ao risco |
| ux-architect | `frontend-design:frontend-design`, `impeccable:impeccable`, `dataviz` | Sistema de design, crítica de UI, visualização de dados |
| devsecops | `commit-commands:commit`, `supabase:supabase` | Disciplina de commit, migrations e pipeline |
| implementer | `superpowers:test-driven-development`, `superpowers:systematic-debugging`, `superpowers:using-git-worktrees` | TDD como regra, debug por causa raiz, isolamento por worktree |
| reviewer | `pr-review-toolkit:review-pr`, `superpowers:verification-before-completion` | Revisores especializados na mesa de Veredito; evidência antes de afirmação |
| grc-reviewer | `security-review`; skills ITXPRO de GRC (`iso27001`, `nist-csf`, `soc2`, `pci-compliance`) quando o domínio pedir | Parecer de conformidade com base em framework real |

## Do harness (do projeto, não de agente)

- `hookify` — transforma os "nunca fazer" da constituição em hooks executáveis: bloquear segredo em commit, bloquear fatia sem spec aprovada, avisar estouro do teto de 120 linhas. Regra escrita vira regra imposta pela máquina.
- `claude-md-management` — auditoria periódica da constituição e do teto de linhas.
- `superpowers:writing-skills` e `skill-creator` — criação das skills próprias da ITXPRO.
- `superpowers:dispatching-parallel-agents` — quando a fase tiver trabalho independente paralelizável.
- `superpowers:finishing-a-development-branch` — fechamento de branch ao fim da fatia.

## Plugins de terceiros: instalação

Fonte única da lista que o setup confere. O script `hooks/check-plugins.py` do plugin lê esta tabela pelo cabeçalho fixo e o registro local de plugins instalados (leitura, nunca instalação) e imprime, para cada ausente, o comando, a fonte e o que degrada sem ele. Cabeçalho fixo: `| Plugin | Fonte oficial | Instalação | Sem ele |`. Uma linha por plugin. Nenhum é pré-requisito: a única dependência dura é o gitleaks.

| Plugin | Fonte oficial | Instalação | Sem ele |
|---|---|---|---|
| `superpowers` | marketplace `claude-plugins-official` | `/plugin install superpowers@claude-plugins-official` | Intenção sem brainstorming, Desenho sem writing-plans, implementer sem TDD e debug sistemático, Veredito sem verification-before-completion |
| `hookify` | marketplace `claude-plugins-official` | `/plugin install hookify@claude-plugins-official` | As regras `.claude/hookify.*.local.md` não rodam: sem bloqueio de `backlog.md` e sem aviso shift-left de segredo (o gate de commit e o CI continuam) |
| `pr-review-toolkit` | marketplace `claude-plugins-official` | `/plugin install pr-review-toolkit@claude-plugins-official` | reviewer sem revisores especializados na mesa de Veredito |
| `commit-commands` | marketplace `claude-plugins-official` | `/plugin install commit-commands@claude-plugins-official` | devsecops sem disciplina de commit assistida |
| `context7` | marketplace `claude-plugins-official` | `/plugin install context7@claude-plugins-official` | architect e implementer sem docs de biblioteca sob demanda; caem na memória do modelo |
| `supabase` | marketplace `claude-plugins-official` | `/plugin install supabase@claude-plugins-official` | architect e devsecops sem skill de stack; só importa se a stack declarada usar |
| `vercel` | marketplace `claude-plugins-official` | `/plugin install vercel@claude-plugins-official` | architect sem skill de stack; só importa se a stack declarada usar |
| `frontend-design` | marketplace `claude-plugins-official` | `/plugin install frontend-design@claude-plugins-official` | ux-architect sem crítica de UI assistida |
| `claude-security` | marketplace `claude-plugins-official` | `/plugin install claude-security@claude-plugins-official` | security-privacy-architect sem varredura sob demanda |
| `claude-md-management` | marketplace `claude-plugins-official` | `/plugin install claude-md-management@claude-plugins-official` | sem auditoria assistida do teto da constituição |
| `skill-creator` | marketplace `claude-plugins-official` | `/plugin install skill-creator@claude-plugins-official` | criação de skills próprias sem assistência |

Fora da tabela, e por isso fora do check: `impeccable` e `dataviz` (fonte oficial não verificada; `impeccable` só apareceu instalado por upload local, `dataviz` sem marketplace conhecido) e as skills ITXPRO de GRC (privadas). Regra: skill do per-agente sem linha nesta tabela não entra no check; entra quando tiver fonte pública verificada. Todo nome da tabela ocorre também na tabela por agente ou na seção "Do harness" deste arquivo (guarda de deriva do gate de referências).

## Não adotados como padrão

- `ralph-loop` — loop autônomo conflita com os portões humanos do fluxo.
- `feature-dev` — pipeline próprio que compete com o fluxo em vez de servi-lo.
- `code-simplifier` como etapa fixa — uso sob demanda do reviewer, não passo automático.
- Plugin de memória automática (claude-mem ou similar) — não entra sem nota de decisão. A memória do projeto é curada e vive em disco (nota `2026-08-14-padroes-nomeados-e-memoria.md`).

## Mecânica de invocação

O condutor invoca a skill da fase antes de convocar a mesa. Os subagentes recebem no mandato a instrução de usar a skill correspondente. Skill de stack (`supabase`, `vercel:nextjs`, `context7`) é consultada no momento da dúvida, não pré-carregada: divulgação progressiva vale também para skills.
