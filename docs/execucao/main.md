
# 🚀 `main.py` – Fluxo Principal de Execução

Este script executa o PyConector de forma autônoma diretamente no terminal. Ele realiza o login, escuta novas mensagens recebidas e responde automaticamente a determinados contatos. É ideal para rodar o PyConector sem API, em modo contínuo.

---

## ⚙️ Descrição do Funcionamento

### 1. Inicialização do PyConector

```python
instance = automation(gui=True)
instance.start()
```
- Cria uma instância do PyConector com interface gráfica (`gui=True`).
- Inicia o navegador controlado pelo Selenium e carrega o WhatsApp Web.

---

### 2. Controle de Mensagens

```python
contatosEncontrados = set()
listaPermitidos = []
```
- `contatosEncontrados`: armazena os contatos que já foram detectados como novos para evitar múltiplas respostas.
- `listaPermitidos`: se preenchida, restringe as respostas apenas aos contatos listados (por nome).

---

### 3. Laço Principal de Escuta

```python
while True:
    novos_contatos = instance.VerificarNovaMensagem()
```
- Verifica continuamente (a cada 3 segundos) se há novas mensagens recebidas na tela principal do WhatsApp.

---

### 4. Detecção de Novas Mensagens

```python
for contato in novos_contatos:
    if contato not in contatosEncontrados:
        print(f"📨 Nova mensagem de: {contato}")
        contatosEncontrados.add(contato)
```
- Para cada contato novo detectado, imprime no terminal e adiciona à lista de contatos a serem respondidos.

---

### 5. Resposta Condicional

```python
if novos_contatos and (not listaPermitidos or any(c in novos_contatos for c in listaPermitidos)):
```
- Se houver novos contatos e:
  - `listaPermitidos` estiver vazia (modo aberto); ou
  - Pelo menos um contato estiver na lista de permitidos.

---

### 6. Interação com o Contato

```python
instance.searchExistsContactAndOpen(contato)
history = instance.pegar_todas_mensagens()
success = instance.enviar_mensagem_para_contato_aberto("ola essa e uma mensagem de teste")
```
- Abre a conversa com o contato.
- Recupera o histórico de mensagens.
- Envia uma mensagem de resposta fixa.
- Se o envio for bem-sucedido, remove o contato da lista de pendentes.

---

### 7. Retorno à Tela Inicial

```python
instance.go_to_home()
```
- Garante que o PyConector volte à tela principal do WhatsApp para continuar escutando novas conversas.

---

## ⏱️ Intervalo de Verificação

```python
time.sleep(3)
```
- Aguarda 3 segundos antes de iniciar um novo ciclo de verificação.

---

## ✅ Comportamento Esperado

- O PyConector responderá apenas uma vez por contato enquanto a sessão estiver ativa.
- Após resposta, o contato é removido da fila `contatosEncontrados`.
- Pode ser adaptado para responder com base em filtros ou análises de conteúdo da mensagem.

---

## 🧪 Requisitos

- Sessão ativa no WhatsApp Web.
- ChromeDriver compatível e configurado corretamente.
- Dependências do projeto instaladas (`pip install -r requirements.txt`).
