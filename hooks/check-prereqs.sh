#!/bin/sh
# Check de pré-requisito dos hooks de enforcement (fatia 001, T01).
# Verifica gitleaks no PATH e versão mínima. Mensagens seguem a anatomia
# fato -> regra -> caminho, com comando de instalação copiável.
# Uso: sh hooks/check-prereqs.sh (a partir da raiz do plugin)

set -u

MIN_VERSION="8.21.0"
INSTALL_VERSION="8.30.1"

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

install_hint() {
  cat <<EOF
Caminho: instale o gitleaks e rode este check de novo.

  # macOS
  brew install gitleaks

  # Linux (binário oficial, ajuste a arquitetura se preciso)
  curl -sSL https://github.com/gitleaks/gitleaks/releases/download/v${INSTALL_VERSION}/gitleaks_${INSTALL_VERSION}_linux_x64.tar.gz | tar -xz gitleaks
  sudo mv gitleaks /usr/local/bin/
EOF
}

# 1. gitleaks presente no PATH
if ! command -v gitleaks >/dev/null 2>&1; then
  {
    echo "Fato: gitleaks não está no PATH."
    echo "Regra: o gate de commit é fail-closed; sem gitleaks, nenhum commit passa (README do plugin itxpro-sdd, seção 'Pré-requisito: gitleaks')."
    install_hint
  } >&2
  exit 1
fi

# 2. versão mínima (compatibilidade de parse do .gitleaks.toml, ver README)
RAW_VERSION="$(gitleaks version 2>/dev/null | tr -d '[:space:]')"
VERSION="${RAW_VERSION#v}"

case "$VERSION" in
  ''|*[!0-9.]*)
    {
      echo "Fato: não consegui ler a versão do gitleaks (saída: '${RAW_VERSION:-vazia}')."
      echo "Regra: a versão mínima é ${MIN_VERSION}, por compatibilidade de parse do .gitleaks.toml."
      install_hint
    } >&2
    exit 1
    ;;
esac

# menor versão entre a instalada e a mínima, via sort -V
LOWEST="$(printf '%s\n%s\n' "$VERSION" "$MIN_VERSION" | sort -V | head -n1)"

if [ "$LOWEST" != "$MIN_VERSION" ]; then
  {
    echo "Fato: gitleaks ${VERSION} instalado; a versão mínima é ${MIN_VERSION}."
    echo "Regra: o .gitleaks.toml compartilhado usa allowlists por regra, sintaxe da 8.21.0 em diante; versão anterior ignora a allowlist em silêncio (README do plugin itxpro-sdd, seção 'Pré-requisito: gitleaks')."
    install_hint
  } >&2
  exit 1
fi

echo "Pré-requisitos OK: gitleaks ${VERSION} (mínimo ${MIN_VERSION})."
exit 0
