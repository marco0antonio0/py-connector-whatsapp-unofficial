from services.bot.bot import automation
import time

# 🧠 Inicializa o bot com interface gráfica (GUI ativada)
instance = automation(gui=True)

# 🔐 Inicia a sessão do WhatsApp Web (requer leitura de QR code no primeiro uso)
instance.start()
print("🤖 Bot iniciado e logado com sucesso!")

# 🗃️ Conjunto para rastrear contatos já respondidos (evita duplicações)
contatosEncontrados = set()

# 🔁 Loop principal de execução contínua do bot
while True:
    # 🔍 Verifica se existem novos contatos com mensagens não lidas
    novos_contatos = instance.VerificarNovaMensagem()

    # 🔔 Notifica e adiciona novos contatos à fila de resposta
    for contato in novos_contatos:
        if contato not in contatosEncontrados:
            print(f"📨 Nova mensagem de: {contato}")
            contatosEncontrados.add(contato)

    # 🔁 Processa cada contato pendente de resposta
    for contato in list(contatosEncontrados):
        try:
            # 🔎 Abre a conversa com o contato
            instance.searchExistsContactAndOpen(contato)

            # 💬 Envia uma mensagem de resposta padrão
            instance.enviar_mensagem_para_contato_aberto("Example message bot test!")
            print(f"✔️ Respondido para {contato}")

            # ✅ Remove o contato da lista após responder
            contatosEncontrados.remove(contato)

            # 🏠 Retorna à tela principal do WhatsApp Web
            instance.go_to_home()

        except Exception as e:
            print(f"❌ Erro ao responder {contato}: {e}")

    # 💤 Aguarda 3 segundos antes de repetir o ciclo
    time.sleep(3)
