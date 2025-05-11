
# ✉️ `example_of_auto_response_to_any_contact.py`

Este exemplo implementa uma rotina simples e eficaz para **responder automaticamente todos os contatos** que enviarem uma nova mensagem, com um texto fixo.

É ideal para respostas automáticas básicas, como mensagens de saudação, ausência, confirmação ou atendimento automático.

---

## 🧠 Lógica do Funcionamento

### 1. Inicialização do PyConector

```python
instance = automation(gui=True)
instance.start()
```

- Inicializa o navegador controlado via Selenium em modo gráfico.
- Inicia o processo de autenticação e carregamento do WhatsApp Web.

---

### 2. Controle de Contatos Respondidos

```python
contatosEncontrados = set()
```

- Armazena os nomes dos contatos que já receberam uma resposta.
- Garante que cada contato será respondido apenas uma vez por ciclo.

---

### 3. Laço de Verificação

```python
novos_contatos = instance.VerificarNovaMensagem()
```

- Escaneia a interface do WhatsApp Web em busca de novos contatos com mensagens não lidas.

```python
for contato in novos_contatos:
    if contato not in contatosEncontrados:
        print(f"📨 Nova mensagem de: {contato}")
        contatosEncontrados.add(contato)
```

- Exibe o nome do contato e o adiciona à fila de resposta.

---

### 4. Resposta Automática

```python
instance.searchExistsContactAndOpen(contato)
instance.enviar_mensagem_para_contato_aberto("Example message bot test!")
```

- Abre a conversa com o contato.
- Envia uma mensagem automática padrão.

```python
contatosEncontrados.remove(contato)
instance.go_to_home()
```

- Após o envio, o contato é removido da fila e o PyConector retorna à tela principal.

---

### 5. Controle de Loop

```python
time.sleep(3)
```

- Aguarda 3 segundos antes de iniciar uma nova verificação.

---

## 💡 Exemplo de Mensagem Padrão

```text
"Example message PyConector test!"
```

Você pode customizar o conteúdo conforme o objetivo do seu PyConector, como:
- "Olá! Em breve retornaremos seu contato."
- "Este número está automatizado. Para suporte, acesse nosso site."
- "Obrigado por entrar em contato!"

---

## 🛠️ Pré-requisitos

- Sessão do WhatsApp Web ativa e autenticada.
- ChromeDriver configurado e compatível.
- Módulos Python instalados via `requirements.txt`.

---

Este script é um ótimo ponto de partida para construir respostas mais complexas ou regras baseadas em análise de conteúdo.