
# 📦 PyConector - Instalação e Inicialização
> ____
> 🔗 **Contato profissional:** [linkedin.com/in/marco-antonio-aa3024233](https://www.linkedin.com/in/marco-antonio-aa3024233)  
> 🔗 **Repositorio-PyConector:** [https://github.com/marco0antonio0/py-connector-whatsapp-unofficial](hhttps://github.com/marco0antonio0/py-connector-whatsapp-unofficial)  
> ____
1. **Clone o repositório**:

   ```bash
   git clone https://github.com/marco0antonio0/py-connector-whatsapp-unofficial
   cd py-connector-whatsapp-unofficial
   ```

2. **Instale as dependências Python**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o script de instalação**:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   🔧 O que o `./install.sh` faz:

   Este script automatiza toda a configuração necessária para que o PyConector funcione corretamente com o Google Chrome e o ChromeDriver compatíveis.

   📋 **Etapas executadas**:

   - Verifica se o Google Chrome está instalado:
     - Caso não esteja, o script baixa o pacote `.deb` diretamente do site oficial do Google e instala com `apt`.

   - Detecta a versão instalada do Google Chrome:
     - Executa `google-chrome --version` e extrai a versão exata para garantir compatibilidade.

   - Monta a URL de download do ChromeDriver oficial:
     - Exemplo de URL:  
       `https://storage.googleapis.com/chrome-for-testing-public/<versão>/linux64/chromedriver-linux64.zip`

   - Cria o diretório `./chromeDrive` e armazena os binários.

   - Baixa, extrai e move o ChromeDriver para `./chromeDrive`.

   - Limpa arquivos temporários (.zip, pastas auxiliares).

   ✅ **Resultado**:
   Ambiente pronto com:
   - Google Chrome instalado (se necessário).
   - ChromeDriver correspondente em `./chromeDrive/`.

4. **Inicie o PyConector**:

   Opções:

   - **Autônomo**:
     ```bash
     python3 main.py
     ```

   - **Via API**:
     ```bash
     python3 api.py
     ```

5. **Acesse o Swagger e veja os endpoints**:

   🌐 [http://localhost:3000/apidocs/](http://localhost:3000/apidocs/)