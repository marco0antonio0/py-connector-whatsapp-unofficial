
# 🖼️ `example_of_sending_image_to_specific_contact.py`

Este exemplo mostra como detectar uma nova mensagem de um contato específico e responder automaticamente com o envio de uma imagem.

É ideal para automatizar o envio de mídia em fluxos pré-definidos ou campanhas de resposta visual.

---

## 🧠 Lógica do Funcionamento

### 1. Inicialização do PyConector

```python
instance = automation(gui=True)
instance.start()
```

- Inicializa o PyConector com interface gráfica (`gui=True`).
- Realiza o login via QR Code e mantém a sessão ativa no navegador.

---

### 2. Detecção de Novas Mensagens

```python
novos_contatos = instance.VerificarNovaMensagem()
```

- Escaneia a tela principal do WhatsApp Web em busca de novas mensagens não lidas.

```python
for contato in novos_contatos:
    if contato not in contatosEncontrados:
        print(f"📨 Nova mensagem de: {contato}")
        contatosEncontrados.add(contato)
```

- Exibe no terminal o nome do contato e adiciona à lista de controle para garantir que o envio seja feito apenas uma vez.

---

### 3. Regra de Envio de Imagem

```python
if contato == "Marco Antonio":
```

- Verifica se o contato é o desejado. Pode ser adaptado para múltiplos nomes.

```python
instance.searchExistsContactAndOpen(contato)
imagem = instance.openImage("./images/teste.png")
instance.sendFigure(imagem)
```

- Abre a conversa com o contato.
- Processa a imagem localizada em `./images/teste.png`.
- Realiza o envio da imagem utilizando `sendFigure`.

---

### 4. Controle de Fluxo

- Após envio, o contato é removido de `contatosEncontrados` para evitar reenvio.
- O PyConector retorna à tela principal com `instance.go_to_home()` para continuar escutando novas mensagens.
- O loop reinicia após um `sleep(3)` para evitar sobrecarga e polling excessivo.

---

## 📂 Pré-requisitos

- A imagem `teste.png` deve estar presente em `./images/`.
- O PyConector deve estar autenticado e com sessão ativa no WhatsApp Web.
- É necessário o ChromeDriver configurado corretamente.

---

## 🧪 Exemplo de Comportamento

| Contato          | Ação                              |
|------------------|-----------------------------------|
| "Marco Antonio"  | Envio automático da imagem `teste.png` |
| Outro contato    | Ignorado                          |

---

## 🛠️ Pré-requisitos

- Sessão do WhatsApp Web ativa e autenticada.
- ChromeDriver configurado e compatível.
- Módulos Python instalados via `requirements.txt`.

---
Este script pode ser adaptado facilmente para envio em massa, respostas personalizadas com mídia ou integração com gatilhos externos.
