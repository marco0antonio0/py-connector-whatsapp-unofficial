#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

############################################
# Termos de Uso
############################################

if [[ -f "eula.txt" ]] && grep -q "Termos aceitos" eula.txt; then
  echo "✅ Termos de uso já aceitos anteriormente:"
  cat eula.txt
else
  echo "📜 Termos de Uso"
  echo "Ao usar este script, você concorda em utilizá-lo de forma responsável e está ciente de que o autor não se responsabiliza por qualquer uso indevido ou danos causados."
  echo "Você aceita os termos de uso? (sim/não)"
  read -rp "❓ Resposta: " resposta

  if [[ "$resposta" != "sim" ]]; then
    echo "🚫 Termos não aceitos. Encerrando o script."
    exit 1
  fi

  echo "✅ Termos aceitos em $(date '+%Y-%m-%d %H:%M:%S')" > eula.txt
  echo "📝 Registro salvo em eula.txt"
fi

############################################
# Instalação/Atualização de Ambiente
############################################

bash ./install.sh

############################################
# Execução do Script
############################################

source .venv/bin/activate

if [ "${1:-}" = "api" ]; then
  echo "🚀 Executando api.py..."
  python3 api.py
else
  echo "🚀 Executando main.py..."
  python3 main.py
fi
