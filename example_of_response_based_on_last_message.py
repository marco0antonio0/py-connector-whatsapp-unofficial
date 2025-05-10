from services.bot.bot import automation
import time
import unicodedata

# 🔧 Inicializa a automação com interface gráfica ativada
instance = automation(gui=True)

# 🔐 Realiza login no WhatsApp Web
instance.start()
print("🤖 Bot iniciado e logado com sucesso!")

# 🗃️ Lista de contatos já verificados para evitar múltiplas respostas
contatosEncontrados = set()

# 🧼 Função utilitária para remover acentos e padronizar texto
def normalizar_texto(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()

# 🔁 Loop contínuo para monitoramento de novas mensagens
while True:
    # 🔍 Busca novos contatos com mensagens não lidas
    novos_contatos = instance.VerificarNovaMensagem()

    for contato in novos_contatos:
        if contato not in contatosEncontrados:
            print(f"📨 Nova mensagem de: {contato}")
            contatosEncontrados.add(contato)

    # 🔁 Itera sobre contatos que ainda não foram respondidos
    for contato in list(contatosEncontrados):
        try:
            # 🔎 Abre a conversa com o contato
            instance.searchExistsContactAndOpen(contato)

            # 🧾 Pega e normaliza o texto da última mensagem recebida
            ultima_msg = normalizar_texto(instance.pegar_ultima_mensagem())

            # 🤖 Define a resposta baseada em palavras-chave
            if "oi" in ultima_msg or "ola" in ultima_msg:
                resposta = "Olá! Como posso ajudar?"
            elif "preco" in ultima_msg or "valor" in ultima_msg:
                resposta = "Nossos preços estão disponíveis em https://meusite.com/precos"
            else:
                resposta = "Desculpe, não entendi. Pode repetir?"

            # 💬 Envia a resposta automaticamente
            instance.enviar_mensagem_para_contato_aberto(resposta)
            print(f"🤖 Resposta enviada: {resposta}")

            # ✅ Remove o contato da fila de espera
            contatosEncontrados.remove(contato)

            # 🏠 Retorna à tela principal
            instance.go_to_home()

        except Exception as e:
            print(f"❌ Erro: {e}")

    # 💤 Espera 3 segundos antes de verificar novamente
    time.sleep(3)
