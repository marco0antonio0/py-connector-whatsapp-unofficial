import time
import traceback

from services.bot.bot import automation
from utils.bootstrap import bootstrap_main_config

config = bootstrap_main_config()

# ==============================
#   INICIALIZAÇÃO DO BOT
# ==============================
instance = automation(gui=config.get("gui", False))
instance.start()

print("=" * 55)
print("               ✅ Logado com sucesso")
print("=" * 55)
print("               🤖 Sistema Iniciado")
print("=" * 55)

contatosEncontrados = set()
listaPermitidos = []
event_queue = []


def processar_contato(contato: str):
    if contato != "Marco Antonio":
        return

    print("📨 Marco mandou mensagem")
    try:
        encontrou = instance.searchExistsContactAndOpen(contato)
        if not encontrou:
            print(f"⚠️ Não foi possível abrir a conversa de '{contato}'.")
            return

        history = instance.pegar_todas_mensagens()
        success = instance.enviar_mensagem_para_contato_aberto("ola essa e uma mensagem de teste")
        print(history)

        if success and contato in contatosEncontrados:
            contatosEncontrados.remove(contato)
    except Exception as e:
        print(f"❌ Erro: {e}")
        traceback.print_exc()
    finally:
        instance.go_to_home()


def on_ready(_payload: dict):
    print("✅ Evento ready recebido")


def on_message(payload: dict):
    contato = payload.get("contact", "").strip()
    if contato:
        event_queue.append(contato)


instance.on("ready", on_ready)
instance.on("message", on_message)

# ==============================
#      LOOP PRINCIPAL
# ==============================
ultimo_fallback = 0.0
while True:
    # Evento DOM (estilo EventEmitter do wwebjs)
    instance.pump_events()

    while event_queue:
        contato = event_queue.pop(0)
        if contato not in contatosEncontrados:
            print(f"📨 Nova mensagem de: {contato}")
            contatosEncontrados.add(contato)
        if not listaPermitidos or contato in listaPermitidos:
            processar_contato(contato)

    # Fallback defensivo: caso observer não capture alguma mutação
    agora = time.time()
    if agora - ultimo_fallback >= 3:
        ultimo_fallback = agora
        novos_contatos = instance.VerificarNovaMensagem()
        for contato in novos_contatos:
            if contato not in contatosEncontrados:
                print(f"📨 Nova mensagem de: {contato}")
                contatosEncontrados.add(contato)
            if not listaPermitidos or contato in listaPermitidos:
                processar_contato(contato)

    time.sleep(1)
