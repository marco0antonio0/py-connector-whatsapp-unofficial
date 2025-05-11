
# 💬 `example_of_response_based_on_last_message.py`

Este exemplo demonstra como o PyConector pode responder de forma **inteligente e contextual**, com base no conteúdo da **última mensagem recebida** em uma conversa do WhatsApp.

O objetivo é personalizar a resposta automática dependendo de palavras-chave simples encontradas na mensagem recebida.

---

## 🧠 Lógica de Funcionamento

### 1. Função de Normalização

```python
from unicodedata import normalize

def normalizar_texto(texto):
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()
```

- Remove acentuação e transforma todo o texto em minúsculas.
- Isso facilita a comparação e identificação de palavras-chave, mesmo que escritas com variações como "Olá", "ola", "OLÁ", etc.

---

### 2. Captura da Última Mensagem

```python
ultima_msg = normalizar_texto(instance.pegar_ultima_mensagem())
```

- Utiliza a função `pegar_ultima_mensagem()` da classe `automation` para buscar a última mensagem da conversa aberta.
- Em seguida, aplica a função `normalizar_texto` para padronizar a entrada.

---

### 3. Definição da Resposta com Base no Conteúdo

```python
if "oi" in ultima_msg or "ola" in ultima_msg:
    resposta = "Olá! Como posso ajudar?"
elif "preco" in ultima_msg or "valor" in ultima_msg:
    resposta = "Veja os preços em https://meusite.com/precos"
else:
    resposta = "Desculpe, não entendi."
```

- A resposta é escolhida com base na presença de palavras-chave específicas na última mensagem.
- Esse comportamento pode ser expandido facilmente para incluir mais palavras ou até integrar modelos de NLP.

---

## 📝 Exemplo de Comportamento

| Mensagem recebida         | Resposta automática                          |
|---------------------------|----------------------------------------------|
| "Oi, tudo bem?"           | "Olá! Como posso ajudar?"                    |
| "Qual o valor do produto" | "Veja os preços em https://meusite.com/precos" |
| "asdf123"                 | "Desculpe, não entendi."                     |

---

## 🛠️ Pré-requisitos

- Sessão do WhatsApp Web ativa e autenticada.
- ChromeDriver configurado e compatível.
- Módulos Python instalados via `requirements.txt`.

---