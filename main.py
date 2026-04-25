import traceback

from services.bot.bot import automation
from utils.bootstrap import bootstrap_main_config
from utils.runtime_messages import print_system_started

config = bootstrap_main_config()
instance = automation(gui=config.get("gui", False))
instance.start()
print_system_started()


@instance.run(block=True)
@instance.hook_new_message()
def on_new_message(payload=None):
    contato = instance.hook_new_message.contato
    print(f"📨 Nova mensagem de: {contato}")

    # Ajuste aqui o contato-alvo para resposta automática
    if contato != "Marco Antonio":
        return

    print("📨 Marco mandou mensagem")
    try:
        encontrou = instance.searchExistsContactAndOpen(contato)
        if not encontrou:
            print(f"⚠️ Não foi possível abrir a conversa de '{contato}'.")
            return

        history = instance.pegar_todas_mensagens()
        success = instance.enviar_mensagem_para_contato_aberto(
            "ola essa e uma mensagem de teste"
        )
        print(history)
        print(f"✅ envio={success}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        traceback.print_exc()
    finally:
        instance.go_to_home()
