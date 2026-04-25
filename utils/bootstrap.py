from utils.cli import (
    etapa_termos,
    _detectar_estado,
    etapa_browser,
    etapa_whatsapp,
    load_config,
)
from services.bot.bot import automation


def bootstrap_main_config() -> dict:
    """
    Fluxo de bootstrap da execução principal:
    - carrega config
    - valida termos
    - verifica sessão atual do WhatsApp
    - executa setup interativo se necessário
    """
    config = load_config()

    if not etapa_termos():
        raise SystemExit(0)

    checker = automation(gui=config.get("gui", False))
    try:
        checker.driver.get(checker.site)
        estado = _detectar_estado(checker, timeout=20)
    finally:
        checker.exit()

    if estado != "logado":
        config = etapa_browser(config)
        etapa_whatsapp(config)
        config = load_config()

    return config

