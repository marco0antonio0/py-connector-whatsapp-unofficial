
# 📦 PyConector - Instalação e Inicialização

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/marco0antonio0/py-connector-whatsapp-unofficial
   cd py-connector-whatsapp-unofficial
   ```

2. **Instale as dependências python**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o script de instalação**:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   🔧 O que o ./install.sh faz:

    Este script automatiza toda a configuração necessária para que o PyConector funcione corretamente com o Google Chrome e o ChromeDriver compatíveis.

    📋 Etapas executadas:

    1. Verifica se o Google Chrome está instalado:
    - Caso não esteja, o script baixa o pacote .deb do Chrome diretamente do site oficial do Google.
    - Em seguida, ele instala automaticamente o navegador via apt.

    2. Detecta a versão instalada do Google Chrome:
    - O script executa google-chrome --version e extrai a versão exata instalada para garantir compatibilidade com o ChromeDriver.

    3. Monta a URL de download do ChromeDriver oficial:
    - Com base na versão instalada do Chrome, é gerada uma URL personalizada de download direto do servidor do Google:
        https://storage.googleapis.com/chrome-for-testing-public/<versão>/linux64/chromedriver-linux64.zip

    4. Cria o diretório ./chromeDrive:
    - Todos os arquivos extraídos do ChromeDriver serão armazenados neste diretório, usado pela automação.

    5. Baixa e extrai o ChromeDriver:
    - O .zip é baixado silenciosamente.
    - O conteúdo é extraído e movido diretamente para a pasta ./chromeDrive.

    6. Remove arquivos temporários:
    - Limpeza automática do .zip baixado e das pastas auxiliares para manter o ambiente limpo.

    ✅ Resultado:
    Após rodar ./install.sh, seu ambiente estará preparado com:
    - Google Chrome instalado (caso não estivesse).
    - ChromeDriver correspondente à versão do Chrome, localizado em ./chromeDrive/.

4. **Inicie o PyConector**:
- Opções:
    - Iniciar a PyConector Autonomo
    - ```bash
        python3 main.py
    - Iniciar a PyConector API
    - ```bash
        python3 api.py
5. **Acesse o swaggerDocs e veja os endpoints**:  
    🌐 **Swagger disponível em:** [http://localhost:3000/apidocs/](http://localhost:3000/apidocs/) 

---

