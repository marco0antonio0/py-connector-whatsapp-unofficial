"""
Exemplos de uso com identificadores de contato (nome, numero, jid, lid).

Executar:
    python3 example_identifier_usage.py
"""

import traceback

from services.bot.bot import automation
from utils.bootstrap import bootstrap_main_config
from utils.runtime_messages import print_system_started


def demo_identificar(instance: automation, identificador: str):
    info = instance.identificar_contato(identificador)
    print(f"\n🔎 identificar_contato('{identificador}')")
    print(info)
    return info


def demo_enviar(instance: automation, identificador: str, texto: str):
    print(f"\n✉️ enviar_mensagem_por_identificador('{identificador}', '{texto}')")
    ok = instance.enviar_mensagem_por_identificador(identificador, texto)
    print(f"resultado={ok}")
    instance.go_to_home()
    return ok


def demo_ler(instance: automation, identificador: str):
    print(f"\n📚 ler_conversa_por_identificador('{identificador}')")
    history = instance.ler_conversa_por_identificador(identificador)
    print(f"mensagens_lidas={len(history)}")
    if history:
        print(f"ultima={history[-1]}")
    instance.go_to_home()
    return history


def run_demo_sync(instance: automation):
    """
    Exemplo síncrono simples:
    - identifica contato
    - abre conversa por identificador
    - lê histórico
    - envia mensagem
    """
    # Troque pelos seus valores reais
    identificador_nome = "Marco Antonio"
    identificador_numero = "+5591999999999"
    identificador_jid = "5591999999999@c.us"
    identificador_lid = "123456789012345@lid"

    demo_identificar(instance, identificador_nome)
    demo_identificar(instance, identificador_numero)
    demo_identificar(instance, identificador_jid)
    demo_identificar(instance, identificador_lid)

    demo_ler(instance, identificador_nome)
    demo_enviar(instance, identificador_nome, "Mensagem teste via identificador")


def run_demo_hook(instance: automation):
    """
    Exemplo por hook em background:
    - recebe novas mensagens
    - resolve identificador automaticamente
    - responde para um contato alvo
    """

    @instance.run(block=False)
    @instance.hook_new_message()
    def on_new_message(payload=None):
        contato = instance.hook_new_message.contato
        info = instance.identificar_contato(contato)
        print(f"\n📨 Nova mensagem de: {contato}")
        print(f"identifier={info}")

        # Ajuste o alvo para seu caso
        if contato != "Marco Antonio":
            return

        try:
            ok = instance.enviar_mensagem_por_identificador(
                contato,
                "Recebi sua mensagem (hook + identificador).",
            )
            print(f"✅ envio_hook={ok}")
        except Exception as e:
            print(f"❌ erro no hook: {e}")
            traceback.print_exc()
        finally:
            instance.go_to_home()

    print("\n🤖 Hook ativo. Pressione CTRL+C para encerrar.")
    instance.wait_forever()


if __name__ == "__main__":
    config = bootstrap_main_config()
    bot = automation(gui=config.get("gui", False))
    bot.start()
    print_system_started()

    # 1) Descomente para rodar o exemplo síncrono:
    # run_demo_sync(bot)

    # 2) Exemplo de hook em background (ativo por padrão):
    run_demo_hook(bot)

