
# 📘 Endpoint da API PyConector WhatsApp
Este projeto é um PyConector de automação do WhatsApp desenvolvido com Selenium WebDriver, permitindo interações automáticas com o WhatsApp Web como envio de mensagens, detecção de novas conversas, leitura de histórico, entre outros.

> ____
> 🔗 **Contato profissional:** [linkedin.com/in/marco-antonio-aa3024233](https://www.linkedin.com/in/marco-antonio-aa3024233)  
> 🌐 **Swagger disponível em:** [http://localhost:3000/apidocs/](http://localhost:3000/apidocs/) (quando executando o projeto localmente)
> ____

## 🔌 Endpoints Detalhados

### ▶️ `POST /start`

Inicia o PyConector na thread principal.

**Resposta:**
```json
{
  "status": "sucesso",
  "mensagem": "Bot iniciado com sucesso."
}
```

---

### 🔐 `POST /login`

Gera e retorna o QRCode de autenticação do WhatsApp Web.

**Resposta:**
```json
{
  "status": "aguardando_login",
  "mensagem": "Bot em execução aguardando leitura do QRCode.",
  "qrCodeUrl": "http://localhost:3000/qrcode/abc123def456.png"
}
```

---

### ✉️ `POST /send`

Envia uma ou mais mensagens para um contato.

**Requisição:**
```json
{
  "contato": "João",
  "mensagens": ["Oi", "Tudo bem?"]
}
```

**Resposta:**
```json
{
  "status": "sucesso",
  "mensagem": "Mensagens enviadas com sucesso.",
  "dados": {
    "historico_mensagens": [
      "Oi",
      "Tudo bem?",
      "Resposta do contato..."
    ]
  }
}
```

---

### 📜 `GET /history/{contato}`

Obtém histórico de mensagens com um contato específico.

**Parâmetros:**
- `contato` (path): Nome do contato para abrir a conversa.

**Resposta:**
```json
{
  "status": "sucesso",
  "mensagem": "Histórico obtido com sucesso.",
  "dados": {
    "mensagens": [
      "Olá!",
      "Como vai?",
      "Tudo certo por aí?"
    ]
  }
}
```

---

### 📡 `GET /status`

Verifica se o PyConector está ativo e se está logado.

**Resposta:**
```json
{
  "status": "ativo",
  "logado": true,
  "mensagem": "Bot está rodando e logado."
}
```

---

### ⛔ `POST /stop`

Finaliza o PyConector e encerra o navegador.

**Resposta:**
```json
{
  "status": "sucesso",
  "mensagem": "Bot finalizado com sucesso."
}
```

---