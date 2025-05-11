
# 🧠 Classe `automation`
> ____
> 🔗 **Contato profissional:** [linkedin.com/in/marco-antonio-aa3024233](https://www.linkedin.com/in/marco-antonio-aa3024233)  
> 🔗 **Repositorio-PyConector:** [https://github.com/marco0antonio0/py-connector-whatsapp-unofficial](hhttps://github.com/marco0antonio0/py-connector-whatsapp-unofficial)  
> ____
Classe principal responsável por gerenciar a automação do WhatsApp Web via Selenium WebDriver. Essa classe encapsula todos os métodos necessários para inicializar o navegador, autenticar com QR Code, enviar mensagens, verificar status e interagir com contatos.

```python
from selenium import webdriver

class automation:
    """Classe principal de automação para WhatsApp Web."""

    def __init__(self, gui=False):
        """
        Inicializa o navegador com as opções definidas.

        Args:
            gui (bool): Se True, abre o navegador com interface gráfica. Caso contrário, roda em modo headless.
        """
```

---

## 🔧 Principais Métodos

### 🔑 Autenticação e Sessão

- **`getDataRef()`**  
  Gera e retorna os dados utilizados na geração do QR Code para login.

- **`login()`**  
  Inicia o processo de login, aguardando a leitura do QR Code. Utilizado na execução do codigo autonomo

- **`checkIsLogin()`**  
  Verifica se o usuário já está logado no WhatsApp Web.

- **`start()`**  
  Executa a rotina completa de inicialização manual da automação.

- **`start_api()`**  
  Executa a inicialização manual adaptada para controle via API.

- **`go_to_home()`**  
  Redireciona o navegador para a tela inicial do WhatsApp após o login.

- **`exit()`**  
  Encerra o navegador e finaliza a sessão atual.

---

### ✉️ Mensagens e Conversas

- **`enviar_mensagem_para_contato_aberto(texto)`**  
  Envia uma mensagem de texto para o contato com a conversa já aberta.

- **`pegar_ultima_mensagem()`**  
  Retorna a última mensagem trocada na conversa aberta.

- **`pegar_todas_mensagens()`**  
  Retorna todo o histórico de mensagens da conversa aberta.

- **`searchExistsContactAndOpen(contato)`**  
  Pesquisa por um contato na lista e abre a conversa.

- **`abrir_conversa_por_nome(contato)`**  
  Acessa diretamente a conversa de um contato pelo nome.

---

### 🖼️ Envio de Mídia

- **`openImage(image_path)`**  
  Abre e processa uma imagem para envio.

- **`sendFigure(midia)`**  
  Envia uma imagem/mídia já processada na conversa atual.

---

### 🔔 Notificações e Monitoramento

- **`VerificarNovaMensagem()`**  
  Verifica se existem novas mensagens na tela principal do WhatsApp e retorna os nomes dos contatos que enviaram.

---

## ⚙️ Configuração Interna

- Usa `ChromeDriver` com suporte a modo **headless**.
- Preserva sessões de usuário via `user-data-dir`.
- Navegador é maximizado e configurado para linguagem `pt-br`.
- Caminho do driver configurado automaticamente com base no diretório do projeto.

---

Essa classe é a base de todas as operações automatizadas do sistema, sendo utilizada tanto na execução manual quanto na execução via endpoints REST expostos pela API Flask.