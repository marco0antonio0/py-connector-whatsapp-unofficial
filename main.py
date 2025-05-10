from services.bot.bot import automation
import time

# ==============================
#   INICIALIZAÇÃO DO BOT
# ==============================
instance = automation(gui=True)
instance.start()

print("=" * 55)
print("               ✅ Logado com sucesso")
print("=" * 55)
print("               🤖 Sistema Iniciado")
print("=" * 55)

# Contatos já notificados
contatosEncontrados = set()

# Lista de contatos permitidos (vazia = todos permitidos)
listaPermitidos = []

# ==============================
#      LOOP PRINCIPAL
# ==============================
while True:
    # Verifica se há novas mensagens
    novos_contatos = instance.VerificarNovaMensagem()

    for contato in novos_contatos:
        if contato not in contatosEncontrados:
            print(f"📨 Nova mensagem de: {contato}")
            contatosEncontrados.add(contato)

    if novos_contatos and (not listaPermitidos or any(c in novos_contatos for c in listaPermitidos)):
        for contato in list(contatosEncontrados):
            if contato == "Marco Antonio":  # <- pode ser dinamizado no futuro
                print("📨 Marco mandou mensagem")

                try:
                    instance.searchExistsContactAndOpen(contato)
                    history = instance.pegar_todas_mensagens()

                    success = instance.enviar_mensagem_para_contato_aberto("ola essa e uma mensagem de teste")
                    print(history)

                    if success:
                        contatosEncontrados.remove(contato)

                except Exception as e:
                    print(f"❌ Erro: {e}")

                finally:
                    instance.go_to_home()

    # Aguarda 3 segundos antes da próxima verificação
    time.sleep(3)
