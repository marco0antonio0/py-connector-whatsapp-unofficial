#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

CHROME_DIR="$ROOT_DIR/chromeDrive"
CHROMEDRIVER_BIN="$CHROME_DIR/chromedriver"
CHROMEDRIVER_VERSION_FILE="$CHROME_DIR/.chromedriver_version"

log() { echo "$1"; }
fail() { echo "❌ $1" >&2; exit 1; }
has_cmd() { command -v "$1" >/dev/null 2>&1; }

require_apt() {
  has_cmd apt || fail "Este script suporta instalação automática apenas em sistemas baseados em apt."
}

install_with_apt_if_missing() {
  local pkg="$1"
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    sudo apt install -y "$pkg"
  fi
}

ensure_prereqs() {
  require_apt
  install_with_apt_if_missing ca-certificates
  install_with_apt_if_missing curl
  install_with_apt_if_missing unzip
  install_with_apt_if_missing grep
  install_with_apt_if_missing gawk
}

chrome_cmd() {
  if has_cmd google-chrome; then
    echo "google-chrome"
  elif has_cmd google-chrome-stable; then
    echo "google-chrome-stable"
  else
    echo ""
  fi
}

install_chrome() {
  require_apt
  log "📥 Baixando pacote do Google Chrome..."
  local tmp_deb
  tmp_deb="$(mktemp --suffix=.deb)"
  curl -fsSL "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -o "$tmp_deb"

  log "⚙️ Instalando Google Chrome..."
  sudo apt install -y "$tmp_deb"
  rm -f "$tmp_deb"
  log "✅ Google Chrome instalado."
}

ensure_chrome() {
  log "🔍 Verificando se o Google Chrome está instalado..."
  if [[ -z "$(chrome_cmd)" ]]; then
    install_chrome
  else
    log "✅ Google Chrome já está instalado."
  fi
}

get_chrome_version() {
  local cmd
  cmd="$(chrome_cmd)"
  [[ -n "$cmd" ]] || fail "Google Chrome não encontrado após tentativa de instalação."
  "$cmd" --version | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
}

ensure_chromedriver() {
  local chrome_version="$1"
  local zip_url="https://storage.googleapis.com/chrome-for-testing-public/${chrome_version}/linux64/chromedriver-linux64.zip"

  mkdir -p "$CHROME_DIR"

  if [[ -x "$CHROMEDRIVER_BIN" ]] && [[ -f "$CHROMEDRIVER_VERSION_FILE" ]]; then
    local cached_version
    cached_version="$(cat "$CHROMEDRIVER_VERSION_FILE" || true)"
    if [[ "$cached_version" == "$chrome_version" ]]; then
      log "✅ ChromeDriver já está atualizado para a versão $chrome_version."
      return 0
    fi
  fi

  log "⬇️ Baixando ChromeDriver $chrome_version..."
  local tmp_dir tmp_zip
  tmp_dir="$(mktemp -d)"
  tmp_zip="$tmp_dir/chromedriver-linux64.zip"
  curl -fsSL "$zip_url" -o "$tmp_zip"

  log "📦 Extraindo ChromeDriver..."
  unzip -q "$tmp_zip" -d "$tmp_dir"

  local extracted_bin="$tmp_dir/chromedriver-linux64/chromedriver"
  [[ -f "$extracted_bin" ]] || fail "Binário do ChromeDriver não encontrado no pacote baixado."

  install -m 0755 "$extracted_bin" "$CHROMEDRIVER_BIN"
  echo "$chrome_version" > "$CHROMEDRIVER_VERSION_FILE"
  rm -rf "$tmp_dir"
  log "✅ ChromeDriver disponível em ./chromeDrive/"
}

ensure_python_and_venv() {
  log "🐍 Verificando se Python 3 está instalado..."
  if ! has_cmd python3; then
    require_apt
    sudo apt install -y python3 python3-pip python3-venv
  else
    log "✅ Python 3 já está instalado."
  fi

  local py_version
  py_version="$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")"
  log "📌 Versão do Python detectada: $py_version"

  if [[ ! -d ".venv" ]]; then
    log "📦 Criando ambiente virtual .venv..."
    python3 -m venv .venv
  elif [[ ! -f ".venv/bin/activate" ]]; then
    fail "Ambiente .venv corrompido (sem .venv/bin/activate). Remova .venv e rode novamente."
  else
    log "✅ Ambiente virtual .venv já existe e está íntegro."
  fi
}

install_python_dependencies() {
  log "⚙️ Ativando ambiente virtual..."
  # shellcheck disable=SC1091
  source .venv/bin/activate

  log "📦 Instalando dependências do requirements.txt..."
  pip install --upgrade pip >/dev/null
  pip install -r requirements.txt
}

main() {
  ensure_prereqs
  ensure_chrome

  local chrome_version
  chrome_version="$(get_chrome_version)"
  log "📌 Versão do Google Chrome instalada: $chrome_version"
  ensure_chromedriver "$chrome_version"

  ensure_python_and_venv
  install_python_dependencies
  log "✅ Ambiente configurado. Pronto para executar."
}

main "$@"
