
# 📱 WhatsApp Automation Bot

> Selenium-powered automation for WhatsApp Web  
> Automação do WhatsApp Web com Selenium

---

### ✅ Overview

This project is a WhatsApp automation bot developed using **Selenium WebDriver**. It allows automated interaction with WhatsApp Web for sending messages, retrieving conversations, detecting new messages, and more.

### 🚀 Features

- **Login Automation**: Automatically logs in and stores session.
- **Send Messages**: Text and media (images/videos).
- **Chat Navigation**: Opens conversations by contact name.
- **QR Code**: Handles login via QR generation.
- **Get Last Message**: Retrieves the latest message from a chat.
- **New Message Detection**: Checks for new messages and prints notifications.

### 📦 Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/marco0antonio0/py-connector-whatsapp-unofficial
   cd py-connector-whatsapp-unofficial
   ```

2. **Install Python Dependencies and Google Chrome**:

   ```bash
   pip install selenium webdriver-manager pillow
   ```

3. **Run Installation Script**:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. **Start the Bot**:

   ```bash
   python3 main.py
   ```

5. **Login with QR Code**:  
   A QR code will be displayed (in GUI mode). Scan it using your WhatsApp mobile app.

---

## 🧪 Usage Examples

```python
from services.bot.bot import automation

bot = automation(gui=True)
bot.start()

bot.searchExistsContactAndOpen("John Doe")
bot.enviar_mensagem_para_contato_aberto("Hello from Python bot!")
history = bot.pegar_ultima_mensagem()
print("Last message:", history)

bot.exit()
```

---

## 📁 Project Structure

```yaml
py-connector-whatsapp-unofficial/
├── main.py
├── install.sh
├── dados/                # Session storage
├── services/
│   ├── bot/
│   │   └── bot.py        # Main automation class
│   └── ...               # Feature modules
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit your changes.
4. Push and open a Pull Request.

---

## 📜 License

MIT License – see [LICENSE](LICENSE)

---

## ✉️ Contact

📧 [marcomesquitajr@hotmail.com](mailto:marcomesquitajr@hotmail.com)

---

### ✅ Visão Geral

Este projeto é um bot de automação do WhatsApp desenvolvido com **Selenium WebDriver**, permitindo interações automáticas com o WhatsApp Web como envio de mensagens, detecção de novas conversas, entre outros.

### 🚀 Funcionalidades

- **Login automático**: Acessa o WhatsApp Web e mantém a sessão.
- **Envio de mensagens**: Texto e mídia (imagens/vídeos).
- **Gerenciamento de conversas**: Abre chats por nome do contato.
- **Geração de QR Code**: Gera o QR para login.
- **Recuperar última mensagem**: Lê a última mensagem do chat.
- **Detecção de mensagens novas**: Verifica novas mensagens.

### 📦 Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/marco0antonio0/py-connector-whatsapp-unofficial
   cd py-connector-whatsapp-unofficial
   ```

2. **Instale as dependências e o Chrome**:

   ```bash
   pip install selenium webdriver-manager pillow
   ```

3. **Execute o script de instalação**:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. **Inicie o Bot**:

   ```bash
   python3 main.py
   ```

5. **Faça login com o QR Code**:  
   Um QR será exibido (modo no modo interface ou modo terminal). Escaneie com o app do WhatsApp.

---

## 🧪 Exemplos de Uso

```python
from services.bot.bot import automation

bot = automation(gui=True)
bot.start()

bot.searchExistsContactAndOpen("João da Silva")
bot.enviar_mensagem_para_contato_aberto("Olá, mensagem automática!")
ultima = bot.pegar_ultima_mensagem()
print("Última mensagem:", ultima)

bot.exit()
```

---

## 📁 Estrutura do Projeto

```yaml
py-connector-whatsapp-unofficial/
├── main.py
├── install.sh
├── dados/                # Armazena a sessão
├── services/
│   ├── bot/
│   │   └── bot.py        # Classe principal
│   └── ...               # Módulos específicos e services
├── requirements.txt
└── README.md
```

---

## 🤝 Contribuindo

1. Faça um fork.
2. Crie uma branch (`git checkout -b nova-funcionalidade`)
3. Faça commits.
4. Suba a branch e abra um Pull Request.

---

## 📜 Licença

Licença MIT – veja [LICENSE](LICENSE)

---

## ✉️ Contato

📧 [marcomesquitajr@hotmail.com](mailto:marcomesquitajr@hotmail.com)