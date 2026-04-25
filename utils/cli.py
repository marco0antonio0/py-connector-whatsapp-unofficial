import os
import json
import time
from datetime import datetime

import questionary
from questionary import Style

CONFIG_FILE = "config.json"
EULA_FILE = "eula.txt"
EULA_ACCEPTED_MARKER = "## ACEITO ##"

DEFAULT_CONFIG = {
    "gui": False,
    "modo": "bot",
    "api_port": 3000,
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


def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return {**DEFAULT_CONFIG, **data}
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
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
    try:
        with open(EULA_FILE, "r") as f:
            return EULA_ACCEPTED_MARKER in f.read()
    except FileNotFoundError:
        return False


def registrar_aceite():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(EULA_FILE, "a") as f:
        f.write(f"\n{EULA_ACCEPTED_MARKER}\n✅ Termos aceitos em {timestamp}\n")


def etapa_termos() -> bool:
    """Exibe os Termos de Uso e solicita aceite. Retorna True se aceito."""
    if eula_foi_aceito():
        return True

    header("Termos de Uso")

    if os.path.exists(EULA_FILE):
        with open(EULA_FILE, "r") as f:
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
    etapa_whatsapp(config)


if __name__ == "__main__":
    main()
