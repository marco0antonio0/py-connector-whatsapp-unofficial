#!/bin/bash

set -e

echo "🔍 Verificando se o Google Chrome está instalado..."

# Função para instalar o Google Chrome se não existir
instalar_chrome() {
  echo "📥 [ETAPA 1] Baixando o pacote .deb do Google Chrome..."
  wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb

  echo "⚙️ [ETAPA 2] Instalando o Google Chrome..."
  sudo apt install -y ./chrome.deb

  echo "🧹 Limpando arquivo .deb..."
  rm chrome.deb

  echo "✅ Google Chrome instalado com sucesso!"
}

# Verifica se o Google Chrome está instalado
if ! command -v google-chrome &> /dev/null; then
  instalar_chrome
else
  echo "✅ Google Chrome já está instalado."
fi

# Obtém a versão do Chrome instalada
echo "🔎 Obtendo versão do Google Chrome..."
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
echo "📌 Versão do Google Chrome instalada: $CHROME_VERSION"

# Monta URL do Chrome para Testes
CHROME_ZIP_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"

echo "🌐 URL para download do Chrome Driver:"
echo "➡️ $CHROME_ZIP_URL"

# Cria diretório de destino
echo "📁 Criando diretório ./chromeDrive para extração..."
mkdir -p ./chromeDrive

# Baixa o zip
echo "⬇️ Baixando chromedriver-linux64.zip..."
wget -q "$CHROME_ZIP_URL" -O chromedriver-linux64.zip

# Extrai temporariamente para pasta oculta
echo "📦 Extraindo temporariamente..."
unzip -q chromedriver-linux64.zip -d ./

# Move os arquivos da subpasta para ./chromeDrive/
echo "📂 Movendo arquivos para ./chromeDrive/..."
mv chromedriver-linux64/* ./chromeDrive/

# Limpa zip e pasta temporária
rm -rf chromedriver-linux64 chromedriver-linux64.zip

echo "✅ ChromeDriver extraído diretamente em: ./chromeDrive/"
