from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import psutil
import subprocess

from .services.getDataRef import getDataRef
from .services.login import login
from .services.checkIsLogin import checkIsLogin
from .services.start import start
from .services.start_api import start_api
from .services.go_to_home import go_to_home
from .services.openImage import openImage
from .services.searchExistsContactAndOpen import searchExistsContactAndOpen
from .services.pegar_ultima_mensagem import pegar_ultima_mensagem
from .services.pegar_todas_mensagens import pegar_todas_mensagens
from .services.VerificarNovaMensagem import VerificarNovaMensagem
from .services.enviar_mensagem_para_contato_aberto import enviar_mensagem_para_contato_aberto
from .services.sendFigure import sendFigure
from .services.abrir_conversa_por_nome import abrir_conversa_por_nome


class automation:
    """Automação do WhatsApp Web via Selenium."""

    def __init__(self, gui: bool = False):
        self.loginStatus = False
        self.site = "https://web.whatsapp.com/"
        self.user_data_dir = os.path.abspath("dados")
        devtools_path = os.path.join(self.user_data_dir, "DevToolsActivePort")

        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    if proc.info['cmdline'] and any(self.user_data_dir in str(arg) for arg in proc.info['cmdline']):
                        subprocess.run(["pkill", "-f", "chrome"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        if os.path.exists(devtools_path):
            try:
                os.remove(devtools_path)
            except OSError:
                pass

        opt = Options()
        if not gui:
            opt.add_argument("--headless=new")
            opt.add_argument("--disable-gpu")
            opt.add_argument("--no-sandbox")
            opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("lang=pt-br")
        opt.add_argument("start-maximized")
        opt.add_argument(f"user-data-dir={self.user_data_dir}")

        driver_path = os.path.abspath("chromeDrive/chromedriver")
        self.driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=opt)

    def getDataRef(self):
        return getDataRef(self)

    def login(self):
        return login(self)

    def checkIsLogin(self):
        return checkIsLogin(self)

    def start(self):
        start(self)

    def start_api(self):
        start_api(self)

    def go_to_home(self):
        go_to_home(self)

    def openImage(self, image_path: str):
        return openImage(self, image_path)

    def sendFigure(self, midia):
        sendFigure(self, midia)

    def enviar_mensagem_para_contato_aberto(self, texto: str) -> bool:
        return enviar_mensagem_para_contato_aberto(self, texto)

    def exit(self):
        self.driver.quit()

    def VerificarNovaMensagem(self) -> list:
        return VerificarNovaMensagem(self)

    def pegar_ultima_mensagem(self):
        return pegar_ultima_mensagem(self)

    def pegar_todas_mensagens(self):
        return pegar_todas_mensagens(self)

    def searchExistsContactAndOpen(self, contato: str):
        searchExistsContactAndOpen(self, contato)

    def abrir_conversa_por_nome(self, contato: str):
        abrir_conversa_por_nome(self, contato)
