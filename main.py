import os
import json
import time
import traceback

CONFIG_FILE = "config.json"


def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


config = load_config()

# ==============================
#   TERMOS DE USO
#   sempre verificado, pulado se
#   já aceito anteriormente
# ==============================
from cli import etapa_termos
if not etapa_termos():
    exit(0)

# ==============================
#   VERIFICAÇÃO DE CONEXÃO
#   abre o Chrome uma vez,
#   checa sessão e se expirou
#   roda etapa 1 + 2 antes de
#   iniciar o bot
# ==============================
from cli import _detectar_estado, etapa_browser, etapa_whatsapp
from services.bot.bot import automation

_check = automation(gui=config.get("gui", False))
_check.driver.get(_check.site)
_estado = _detectar_estado(_check, timeout=20)
_check.exit()

if _estado != "logado":
    config = etapa_browser(config)
    etapa_whatsapp(config)
    config = load_config()

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
