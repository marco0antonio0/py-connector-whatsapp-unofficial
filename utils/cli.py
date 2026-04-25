import os
import json
import time
from datetime import datetime

import questionary
from questionary import Style

CONFIG_FILE = os.getenv("CONFIG_FILE", "config.json")
EULA_FILE = os.getenv("EULA_FILE", "eula.txt")
EULA_ACCEPTED_MARKER = "## ACEITO ##"

DEFAULT_CONFIG = {
    "gui": False,
    "modo": "bot",
    "api_port": 3000,
    "webhook_url": "",
    "api_key": "",
}

CLI_STYLE = Style([
    ("qmark", "fg:#00e676 bold"),
    ("question", "bold"),
    ("answer", "fg:#00e676 bold"),
    ("pointer", "fg:#00e676 bold"),
    ("highlighted", "fg:#00e676 bold"),
    ("selected", "fg:#00e676"),
    ("separator", "fg:#555555"),
    ("instruction", "fg:#888888"),
])


def _normalize_file_path(path: str, fallback_name: str) -> str:
    # Se receber um diretório por engano, grava arquivo dentro dele.
    if os.path.isdir(path):
        return os.path.join(path, fallback_name)
    return path


def _ensure_parent_dir(path: str):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def load_config() -> dict:
    path = _normalize_file_path(CONFIG_FILE, "config.json")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return {**DEFAULT_CONFIG, **data}
        except (json.JSONDecodeError, OSError):
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    path = _normalize_file_path(CONFIG_FILE, "config.json")
    _ensure_parent_dir(path)
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def header(etapa: str = ""):
    clear()
    print("\033[1;32m")
    print("  ╔══════════════════════════════════════╗")
    print("  ║     WhatsApp Bot  —  Setup inicial   ║")
    print("  ╚══════════════════════════════════════╝")
    print("\033[0m")
    if etapa:
        print(f"  {etapa}\n")


def eula_foi_aceito() -> bool:
    path = _normalize_file_path(EULA_FILE, "eula.txt")
    try:
        with open(path, "r") as f:
            return EULA_ACCEPTED_MARKER in f.read()
    except FileNotFoundError:
        return False


def registrar_aceite():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = _normalize_file_path(EULA_FILE, "eula.txt")
    _ensure_parent_dir(path)
    with open(path, "a") as f:
        f.write(f"\n{EULA_ACCEPTED_MARKER}\n✅ Termos aceitos em {timestamp}\n")


def etapa_termos() -> bool:
    """Exibe os Termos de Uso e solicita aceite. Retorna True se aceito."""
    if eula_foi_aceito():
        return True

    header("Termos de Uso")

    eula_path = _normalize_file_path(EULA_FILE, "eula.txt")
    if os.path.exists(eula_path):
        with open(eula_path, "r") as f:
            termos = f.read()
        # Exibe os termos paginados (60 linhas por vez)
        linhas = termos.splitlines()
        pagina = 0
        tamanho = 30
        total = len(linhas)

        while pagina * tamanho < total:
            header("Termos de Uso  —  use ↑↓ para rolar")
            bloco = linhas[pagina * tamanho: (pagina + 1) * tamanho]
            for linha in bloco:
                print(f"  {linha}")
            print()

            inicio = pagina * tamanho + 1
            fim = min((pagina + 1) * tamanho, total)
            opcoes = []
            if fim < total:
                opcoes.append("Continuar lendo ↓")
            opcoes.append("Aceitar os Termos de Uso")
            opcoes.append("Recusar e sair")

            acao = questionary.select(
                f"  Linha {inicio}–{fim} de {total}",
                choices=opcoes,
                style=CLI_STYLE,
            ).ask()

            if acao is None or acao == "Recusar e sair":
                clear()
                print("  Você recusou os Termos de Uso.")
                print("  O software não pode ser utilizado sem aceite.\n")
                return False

            if acao == "Aceitar os Termos de Uso":
                break

            pagina += 1

    # Confirmação final
    header("Termos de Uso  —  Confirmação")
    print("  Ao aceitar, você declara que:\n")
    print("  • Leu e compreendeu os Termos de Uso na íntegra;")
    print("  • Utilizará o software apenas para fins lícitos;")
    print("  • Está ciente dos riscos de uso de automação não oficial.\n")

    confirmou = questionary.confirm(
        "Aceita os Termos de Uso?",
        default=False,
        style=CLI_STYLE,
    ).ask()

    if not confirmou:
        clear()
        print("  Você recusou os Termos de Uso.")
        print("  O software não pode ser utilizado sem aceite.\n")
        return False

    registrar_aceite()
    header("Termos de Uso")
    print("  \033[1;32m✔ Termos aceitos. Prosseguindo com o setup...\033[0m\n")
    time.sleep(1)
    return True


def _detectar_estado(bot, timeout: int = 30) -> str:
    """
    Aguarda a página carregar e retorna:
      'logado'  — sessão ativa detectada
      'qr'      — QR code disponível para scan
      'timeout' — nenhum dos dois apareceu
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        if bot.checkIsLogin():
            return "logado"
        if bot.getDataRef():
            return "qr"
        time.sleep(1)
    return "timeout"


def _aguardar_login(bot, tentativas: int = 15) -> bool:
    for _ in range(tentativas):
        if bot.checkIsLogin():
            return True
        time.sleep(2)
    return False


# ──────────────────────────────────────────
#  Etapa 1 — modo do browser
# ──────────────────────────────────────────
def etapa_browser(config: dict) -> dict:
    header("Etapa 1 de 2  →  Modo do browser")

    opcao = questionary.select(
        "Como o Chrome deve rodar?",
        choices=[
            "Headless  (sem janela — recomendado para servidor)",
            "Visível   (abre a janela do Chrome)",
        ],
        default=(
            "Visível   (abre a janela do Chrome)"
            if config["gui"]
            else "Headless  (sem janela — recomendado para servidor)"
        ),
        style=CLI_STYLE,
    ).ask()

    if opcao is None:
        return config

    config["gui"] = opcao.startswith("Visível")
    save_config(config)
    return config


# ──────────────────────────────────────────
#  Etapa API — api_key e webhook_url
# ──────────────────────────────────────────
def etapa_api_preferencias(config: dict) -> dict:
    header("Configuração da API  →  Chave e Webhook")
    print("  Defina as preferências da API.\n")
    print("  • Ambos os campos são opcionais.")
    print("  • Se deixar em branco, será salvo como string vazia.\n")

    api_key = questionary.text(
        "API Key (opcional):",
        default=(config.get("api_key") or ""),
        style=CLI_STYLE,
    ).ask()
    if api_key is None:
        api_key = ""

    webhook_url = questionary.text(
        "Webhook URL (opcional):",
        default=(config.get("webhook_url") or ""),
        style=CLI_STYLE,
    ).ask()
    if webhook_url is None:
        webhook_url = ""

    config["api_key"] = api_key.strip()
    config["webhook_url"] = webhook_url.strip()
    save_config(config)
    return config


# ──────────────────────────────────────────
#  Etapa 2 — conectar ao WhatsApp
# ──────────────────────────────────────────
def etapa_whatsapp(config: dict):
    from services.bot.bot import automation
    from services.generateQRcode import createQRCODE

    header("Etapa 2 de 2  →  Conexão com o WhatsApp")
    print("  Iniciando o Chrome, aguarde...\n")

    bot = automation(gui=config["gui"])
    bot.driver.get(bot.site)

    header("Etapa 2 de 2  →  Conexão com o WhatsApp")
    print("  Verificando sessão, aguarde...\n")

    estado = _detectar_estado(bot)

    if estado == "logado":
        config["setup_done"] = True
        save_config(config)
        header("Etapa 2 de 2  →  Conexão com o WhatsApp")
        print("  \033[1;32m✔ Dispositivo já conectado!\033[0m\n")
        questionary.select(
            "Tudo certo, pode iniciar o bot.",
            choices=["OK"],
            style=CLI_STYLE,
        ).ask()
        bot.exit()
        return

    if estado == "timeout":
        header("Etapa 2 de 2  →  Conexão com o WhatsApp")
        print("  \033[1;31m✗ Não foi possível carregar o WhatsApp Web.\033[0m")
        print("  Verifique sua conexão e tente novamente.\n")
        questionary.press_any_key_to_continue(style=CLI_STYLE).ask()
        bot.exit()
        return

    # estado == "qr" — loop do QR code
    while True:
        qr_data = bot.getDataRef()

        # QR sumiu enquanto esperávamos — verificar se logou
        if not qr_data:
            if bot.checkIsLogin():
                _tela_conectado(config)
                bot.exit()
                return
            # Recarrega para obter novo QR
            bot.driver.get(bot.site)
            time.sleep(3)
            qr_data = bot.getDataRef()
            if not qr_data:
                continue

        header("Etapa 2 de 2  →  Conexão com o WhatsApp")
        print("  Escaneie o QR Code com o WhatsApp no seu celular:\n")
        print("  " + "─" * 44)
        createQRCODE(qr_data)
        print("  " + "─" * 44 + "\n")

        acao = questionary.select(
            "O que deseja fazer?",
            choices=[
                "Já conectei  ✓",
                "Atualizar QR Code",
                questionary.Separator(),
                "Cancelar setup",
            ],
            style=CLI_STYLE,
        ).ask()

        if acao is None or acao == "Cancelar setup":
            bot.exit()
            return

        elif acao == "Já conectei  ✓":
            header("Etapa 2 de 2  →  Verificando conexão...")
            print("  Verificando login, aguarde...\n")
            if _aguardar_login(bot):
                _tela_conectado(config)
                bot.exit()
                return
            else:
                header("Etapa 2 de 2  →  Conexão com o WhatsApp")
                print("  \033[1;33m⚠ Login ainda não detectado.\033[0m")
                print("  Tente escanear novamente.\n")
                questionary.press_any_key_to_continue(style=CLI_STYLE).ask()

        elif acao == "Atualizar QR Code":
            bot.driver.get(bot.site)
            time.sleep(3)


def _tela_conectado(config: dict):
    config["setup_done"] = True
    save_config(config)
    header("Etapa 2 de 2  →  Conexão com o WhatsApp")
    print("  \033[1;32m✔ Conectado com sucesso!\033[0m\n")
    print("  A sessão foi salva. O bot iniciará automaticamente.\n")
    questionary.select(
        "Setup concluído.",
        choices=["OK"],
        style=CLI_STYLE,
    ).ask()


# ──────────────────────────────────────────
#  Entrada principal
# ──────────────────────────────────────────
def main():
    if not etapa_termos():
        return
    config = load_config()
    config = etapa_browser(config)
    config = etapa_api_preferencias(config)
    etapa_whatsapp(config)


if __name__ == "__main__":
    main()
