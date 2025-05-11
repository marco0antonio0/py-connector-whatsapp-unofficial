
# 🤖 Execução Autônoma

O modo de **execução autônoma** permite rodar o PyConector diretamente via terminal, sem depender de requisições externas à API Flask. 
Essa abordagem é ideal para testes locais, automações simples ou comportamentos contínuos de escuta e resposta.

A classe `automation`, responsável por controlar o WhatsApp Web via Selenium, é a mesma utilizada na versão com API. No entanto, aqui o fluxo de controle e lógica estão contidos diretamente nos scripts Python.

> ____
> 🔗 **Contato profissional:** [linkedin.com/in/marco-antonio-aa3024233](https://www.linkedin.com/in/marco-antonio-aa3024233)  
> 🔗 **Repositorio-PyConector:** [https://github.com/marco0antonio0/py-connector-whatsapp-unofficial](hhttps://github.com/marco0antonio0/py-connector-whatsapp-unofficial)  
> ____
---

## 📂 Exemplos incluídos

- **`main.py`**  
  Executa o fluxo completo: login, escuta de mensagens e resposta automática.

- **`example_of_auto_response_to_any_contact.py`**  
  Detecta qualquer novo contato com mensagem recebida e responde com um texto fixo.

- **`example_of_sending_image_to_specific_contact.py`**  
  Demonstra como abrir uma conversa específica e enviar uma imagem.

- **`example_of_response_based_on_last_message.py`**  
  Analisa o conteúdo da última mensagem recebida e responde de forma contextual.

---

## ⚠️ Observação Importante

Todos os exemplos pressupõem que o PyConector esteja **logado no WhatsApp Web** via leitura de QR Code. 
A sessão deve estar ativa no navegador controlado pelo Selenium, com o perfil persistido na pasta `dados/`.

---

Este modo é ideal para criar automações simples e diretas, sem overhead de servidor, especialmente em scripts agendados ou testes locais.