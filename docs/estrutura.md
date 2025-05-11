
# 📁 Estrutura do Projeto

Abaixo está a estrutura principal do repositório `py-connector-whatsapp-unofficial`, destacando os diretórios e arquivos mais relevantes para o funcionamento da automação via API.

> ____
> 🔗 **Contato profissional:** [linkedin.com/in/marco-antonio-aa3024233](https://www.linkedin.com/in/marco-antonio-aa3024233)  
> 🔗 **Repositorio-PyConector:** [https://github.com/marco0antonio0/py-connector-whatsapp-unofficial](hhttps://github.com/marco0antonio0/py-connector-whatsapp-unofficial)  
> ____

```
py-connector-whatsapp-unofficial/
├─ api.py                          # API Flask (rotas e integração com o PyConector)
├─ main.py                         # Execução direta do PyConector autonomo
├─ requirements.txt                # Dependências do projeto
├─ install.sh                      # Script de instalação 
├─ swagger.yml                     # documentação interativa Swagger
│
├─ services/                       # Lógica da automação e subcomponentes
│  ├─ bot/
│  │  ├─ bot.py                    # Classe principal 'automation'
│  │  └─ services/                 # Módulos específicos usados pela automação
│  │     ├─ login.py
│  │     ├─ checkIsLogin.py
│  │     ├─ getDataRef.py
│  │     ├─ pegar_todas_mensagens.py
│  │     ├─ enviar_mensagem_para_contato_aberto.py
│  │     └─ ...
│  └─ generateQRcode.py           # Geração manual de QRCode via terminal
│
├─ static/
│  └─ qrcodes/                     # Armazena imagens temporárias de QRCode
│     └─ <uuid>.png
│
├─ utils/
│  └─ normalizarMessages.py       # Função utilitária para limpeza e normalização de texto
│
├─ chromeDrive/                   # WebDriver do ChromeDrive(baixado pelo script de instalação)
│  ├─ chromedriver
│  ├─ LICENSE.chromedriver
│  └─ THIRD_PARTY_NOTICES.chromedriver
│
├─ dados/                         # Diretório persistente do perfil de usuário do Chrome De sessão
│  └─ ...
│
├─ images/
│  └─ teste.png                   # Imagem de exemplo para envio
│
├─ exemplos/                      # Exemplos práticos de uso
├─ example_of_auto_response_to_any_contact.py      # Exemplos práticos de uso PyConector autonomo
├─ example_of_response_based_on_last_message.py    # Exemplos práticos de uso PyConector autonomo
├─ example_of_sending_image_to_specific_contact.py # Exemplos práticos de uso PyConector autonomo
│
├─ README.md                      # Descrição principal do projeto
├─ LEARN.md                       # Rascunhos ou notas de aprendizado
└─ License.md                     # Licença do projeto
```

---

## 📌 Principais Componentes

- **`services.bot.bot`**  
  Contém a classe `automation`, responsável por controlar todas as ações com o WhatsApp Web.

- **`services.bot.services/`**  
  Cada arquivo representa uma funcionalidade separada, como login, envio de mensagens ou verificação de status.

- **`static/qrcodes/`**  
  Diretório onde os QR Codes gerados temporariamente são salvos e servidos pela API.

- **`swagger.yml`**  
  Define a documentação OpenAPI da API Flask, utilizada pelo Swagger UI.

- **`api.py`**  
  Contém as rotas da API Flask que interagem com a automação.

- **`main.py`**  
  Permite iniciar o PyConector diretamente sem expor via API — útil para testes manuais ou uso autonomo.