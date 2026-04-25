import os
import json
import time

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

# ==============================
#      LOOP PRINCIPAL
# ==============================
while True:
    novos_contatos = instance.VerificarNovaMensagem()

    for contato in novos_contatos:
        if contato not in contatosEncontrados:
            print(f"📨 Nova mensagem de: {contato}")
            contatosEncontrados.add(contato)

    if novos_contatos and (not listaPermitidos or any(c in novos_contatos for c in listaPermitidos)):
        for contato in list(contatosEncontrados):
            if contato == "Marco Antonio":
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

    time.sleep(3)
