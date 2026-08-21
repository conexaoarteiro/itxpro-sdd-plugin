# Cartão de padrão — Fundação: headers de segurança e CSP

> Herdado no setup; consulte na mesa de Desenho de toda fatia com página pública. O piso por classe do fluxo exige estes headers verificados, nunca presumidos.
> Versão: 1.0 · Revisado: 2026-08-20 · Gatilho de revisão: release do plugin · Dono: security-privacy-architect

## Contexto

Página pública sem headers de segurança é fatia descoberta, não fatia leve. Este cartão fixa a lista mínima e o ponto de aplicação, para que nenhuma fatia recrie ou esqueça o baseline.

## Nosso padrão

- Lista mínima em toda resposta de página pública:
  - `Content-Security-Policy` partindo de `default-src 'self'`, cada exceção justificada no plano; `frame-ancestors` restrito (`'none'` até existir motivo).
  - `Strict-Transport-Security` (HSTS) com `max-age` de pelo menos seis meses.
  - `X-Content-Type-Options: nosniff`.
  - `Referrer-Policy: strict-origin-when-cross-origin` ou mais restrito.
- Aplicação por topologia, num ponto só, o declarado na constituição do projeto: proxy reverso quando existe, configuração da plataforma gerenciada, ou middleware do framework web. Dois pontos competindo é bug de configuração.
- Verificado, nunca presumido: fatia com página pública prova os headers em resposta real; é o piso da classe leve.

## Proibido

- Página pública sem CSP; classe leve nunca dispensa os headers do piso.
- Afrouxar a CSP (`unsafe-inline`, curinga de origem) sem escalada; fatia endurece controle da fundação, nunca afrouxa por conveniência.

## Exige nota de decisão

- Exceção de CSP para script, estilo ou frame de terceiro.

## Como verificar herança

- Arquivo: o ponto de aplicação da topologia (config do proxy, da plataforma ou middleware) com os headers declarados.
- Comando: `curl -sI <url pública do projeto>` e conferir os quatro headers na resposta.
