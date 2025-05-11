
# 📘 API - Visão Geral

Esta API foi desenvolvida com **Flask** e integra automação via **Selenium WebDriver** para interações automatizadas com o **WhatsApp Web**. Seu principal objetivo é fornecer uma interface simples e poderosa para iniciar sessões, autenticar via QR Code, enviar mensagens e consultar o status ou histórico de conversas de forma programática.

A arquitetura foi projetada com foco em **concorrência controlada**, utilizando `Queue` e `Thread`, garantindo que apenas uma tarefa seja executada por vez. Isso evita conflitos e garante estabilidade mesmo em operações contínuas com o navegador.
> ____
> 🔗 **Contato profissional:** [linkedin.com/in/marco-antonio-aa3024233](https://www.linkedin.com/in/marco-antonio-aa3024233)  
> 🔗 **Repositorio-PyConector:** [https://github.com/marco0antonio0/py-connector-whatsapp-unofficial](hhttps://github.com/marco0antonio0/py-connector-whatsapp-unofficial)  
> ____
---

## 🔧 Funcionalidades Principais

A API expõe rotas RESTful que permitem:

- `POST /start`: Inicia o PyConector e carrega o WhatsApp Web.
- `POST /login`: Gera e disponibiliza o QR Code para autenticação.
- `POST /send`: Envia uma ou mais mensagens para um contato específico.
- `GET /status`: Retorna se o PyConector está rodando e se está logado.
- `GET /history/<contato>`: Recupera todas as mensagens trocadas com um contato.
- `POST /stop`: Encerra a sessão e finaliza o PyConector.

---

## 🛠️ Tecnologias Utilizadas

- **Flask** – Framework web para construção da API.
- **Selenium WebDriver** – Utilizado para automatizar o navegador e controlar o WhatsApp Web.
- **Flasgger** – Geração automática da documentação Swagger.
- **Threading + Queue** – Controla a execução sequencial de tarefas no backend.
- **qrcode** – Criação de QR Codes temporários para autenticação no WhatsApp.

---

## 📚 Documentação Interativa

Uma interface interativa e pronta para testes está disponível através do Swagger:

🌐 [`http://localhost:3000/apidocs/`](http://localhost:3000/apidocs/)

---

Esta visão geral oferece um panorama rápido da estrutura e capacidades da API, sendo ideal para desenvolvedores que desejam incorporar automação do WhatsApp em seus projetos de forma simples e controlada.