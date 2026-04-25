import os

from utils.cli import (
    etapa_termos,
    _detectar_estado,
    etapa_browser,
    etapa_api_preferencias,
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
    non_interactive = os.getenv("NON_INTERACTIVE", "").strip() in {"1", "true", "TRUE", "yes", "YES"}

    if non_interactive:
        return config

    if not etapa_termos():
        raise SystemExit(0)

    # Permite configurar API key/webhook via CLI no primeiro bootstrap,
    # mesmo quando a sessão do WhatsApp já está logada.
    if not (config.get("api_key") or "").strip() and not (config.get("webhook_url") or "").strip():
        config = etapa_api_preferencias(config)

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
