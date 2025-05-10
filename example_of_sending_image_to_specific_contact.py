from services.bot.bot import automation
import time

# 🔧 Inicializa o bot em modo gráfico (GUI=True)
instance = automation(gui=True)

# 🔐 Inicia o processo de login e aguarda a autenticação via QR Code
instance.start()
print("🤖 Bot iniciado e logado com sucesso!")

# 🗃️ Conjunto para controlar contatos que já foram tratados
contatosEncontrados = set()

# 🔁 Loop contínuo para verificação de novas mensagens
while True:
    # 🔍 Verifica se há novos contatos com mensagens não lidas
    novos_contatos = instance.VerificarNovaMensagem()

    # 🔔 Notifica e armazena novos contatos detectados
    for contato in novos_contatos:
        if contato not in contatosEncontrados:
            print(f"📨 Nova mensagem de: {contato}")
            contatosEncontrados.add(contato)

    # 🧠 Regra personalizada para envio de imagem
    for contato in list(contatosEncontrados):
        if contato == "Marco Antonio":
            print("📸 Enviando imagem para Marco Antonio")
            try:
                # 🔎 Abre a conversa com o contato
                instance.searchExistsContactAndOpen(contato)

                # 🖼️ Processa e prepara a imagem para envio
                imagem = instance.openImage("./images/teste.png")

                # 📤 Envia a imagem carregada
                instance.sendFigure(imagem)

                # ✅ Remove o contato da lista para evitar reenvio
                contatosEncontrados.remove(contato)

                # 🏠 Retorna à tela principal
                instance.go_to_home()

            except Exception as e:
                print(f"❌ Erro ao enviar imagem: {e}")

    # 💤 Aguarda 3 segundos antes de verificar novamente
    time.sleep(3)
