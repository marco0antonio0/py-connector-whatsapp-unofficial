#!/bin/bash

set -e

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
# Google Chrome
############################################

echo "🔍 Verificando se o Google Chrome está instalado..."

instalar_chrome() {
  echo "📥 [ETAPA 1] Baixando o pacote .deb do Google Chrome..."
  wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb

  echo "⚙️ [ETAPA 2] Instalando o Google Chrome..."
  sudo apt install -y ./chrome.deb

  echo "🧹 Limpando arquivo .deb..."
  rm chrome.deb

  echo "✅ Google Chrome instalado com sucesso!"
}

if ! command -v google-chrome &> /dev/null; then
  instalar_chrome
else
  echo "✅ Google Chrome já está instalado."
fi

echo "🔎 Obtendo versão do Google Chrome..."
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
echo "📌 Versão do Google Chrome instalada: $CHROME_VERSION"

CHROME_ZIP_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"
echo "🌐 URL do ChromeDriver: $CHROME_ZIP_URL"

echo "📁 Criando diretório ./chromeDrive..."
mkdir -p ./chromeDrive

echo "⬇️ Baixando ChromeDriver..."
wget -q "$CHROME_ZIP_URL" -O chromedriver-linux64.zip

echo "📦 Extraindo ChromeDriver..."
unzip -q chromedriver-linux64.zip -d ./

echo "📂 Movendo ChromeDriver para ./chromeDrive/..."
mv chromedriver-linux64/* ./chromeDrive/
rm -rf chromedriver-linux64 chromedriver-linux64.zip
echo "✅ ChromeDriver disponível em ./chromeDrive/"

############################################
# Python e Ambiente Virtual
############################################

echo "🐍 Verificando se Python 3 está instalado..."
if ! command -v python3 &> /dev/null; then
  echo "⚙️ Instalando Python 3..."
  sudo apt install -y python3 python3-pip
else
  echo "✅ Python 3 já está instalado."
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
echo "📌 Versão do Python detectada: $PYTHON_VERSION"

echo "🧪 Verificando se .venv existe e está íntegro..."
if [ -d ".venv" ]; then
  if [ -f ".venv/bin/activate" ]; then
    echo "✅ Ambiente virtual .venv já existe e está íntegro."
  else
    echo "❌ Ambiente virtual está corrompido (sem .venv/bin/activate). Corrija manualmente ou remova."
    exit 1
  fi
else
  echo "📦 Criando ambiente virtual .venv..."

  if ! python3 -m ensurepip --version &>/dev/null; then
    echo "⚠️ ensurepip ausente. Instalando python${PYTHON_VERSION}-venv..."

    if ! apt-cache show python${PYTHON_VERSION}-venv &>/dev/null; then
      echo "ℹ️ Repositório universe não encontrado. Habilitando..."
      sudo add-apt-repository universe -y
      sudo apt update
    fi

    if ! sudo apt install -y "python${PYTHON_VERSION}-venv"; then
      echo "❌ Falha ao instalar python${PYTHON_VERSION}-venv."
      echo "💡 Tente instalar manualmente:"
      echo "    sudo apt install -y python${PYTHON_VERSION}-venv"
      exit 1
    fi

    # Verifica de novo
    if ! python3 -m ensurepip --version &>/dev/null; then
      echo "❌ Ainda sem ensurepip mesmo após instalar venv. Abortando."
      exit 1
    fi
  fi

  if ! python3 -m venv .venv; then
    echo "❌ Erro ao criar ambiente virtual com venv."
    exit 1
  fi
fi

echo "⚙️ Ativando ambiente virtual..."
source .venv/bin/activate

echo "📦 Instalando dependências do requirements.txt..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

echo "✅ Ambiente configurado. Pronto para executar."

############################################
# Execução do Script
############################################

if [ "$1" = "api" ]; then
  echo "🚀 Executando api.py..."
  python3 api.py
else
  echo "🚀 Executando main.py..."
  python3 main.py
fi
