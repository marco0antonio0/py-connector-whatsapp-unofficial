from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import os

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
    """Classe principal de automação para WhatsApp Web."""

    def __init__(self, gui=False):
        """
        Inicializa o navegador com as opções definidas.

        Args:
            gui (bool): Se True, abre com interface gráfica. Caso contrário, headless.
        """
        self.loginStatus = False
        self.site = "https://web.whatsapp.com/"

        opt = Options()
        if not gui:
            opt.add_argument("--headless=new")
            opt.add_argument("--disable-gpu")
            opt.add_argument("--no-sandbox")
            opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("lang=pt-br")
        opt.add_argument("user-data-dir=dados")
        opt.add_argument("start-maximized")

        driver_path = os.path.join(os.getcwd(), "chromeDrive/chromedriver")
        chrome_service = ChromeService(executable_path=driver_path)

        self.driver = webdriver.Chrome(service=chrome_service, options=opt)

    def getDataRef(self):
        """Obtém os dados de referência do QRCode de login."""
        return getDataRef(self)

    def login(self):
        """Realiza o login e retorna True se for bem-sucedido, False caso contrário."""
        return login(self)

    def checkIsLogin(self):
        """Verifica se já está logado na sessão do WhatsApp Web."""
        return checkIsLogin(self)

    def start(self):
        """Inicia o processo de login e validação."""
        start(self)

    def start_api(self):
        """Inicia para api"""
        start_api(self)

    def go_to_home(self):
        """Navega para a tela principal do WhatsApp Web."""
        go_to_home(self)

    def openImage(self, image_path):
        """
        Abre uma imagem do caminho especificado.

        Args:
            image_path (str): Caminho completo do arquivo de imagem.
        
        Returns:
            objeto de imagem processado
        """
        return openImage(self, image_path)

    def sendFigure(self, midia):
        """
        Envia uma mídia já processada na conversa atual.

        Args:
            midia: objeto de mídia retornado por `openImage`.
        """
        sendFigure(self, midia)

    def enviar_mensagem_para_contato_aberto(self, texto):
        """
        Envia uma mensagem de texto na conversa atualmente aberta.

        Args:
            texto (str): Conteúdo da mensagem.
        
        Returns:
            bool: True se enviada com sucesso.
        """
        return enviar_mensagem_para_contato_aberto(self, texto)

    def exit(self):
        """Encerra o navegador e finaliza a sessão."""
        self.driver.quit()

    def VerificarNovaMensagem(self):
        """
        Verifica se há novas mensagens na tela principal.

        Returns:
            list: Lista com nomes dos contatos que enviaram novas mensagens.
        """
        return VerificarNovaMensagem(self)

    def pegar_ultima_mensagem(self):
        """Obtém a última mensagem da conversa aberta."""
        return pegar_ultima_mensagem(self)

    def pegar_todas_mensagens(self):
        """Retorna todas as mensagens da conversa atual."""
        return pegar_todas_mensagens(self)

    def searchExistsContactAndOpen(self, contato):
        """
        Pesquisa um contato e abre a conversa correspondente.

        Args:
            contato (str): Nome do contato a ser pesquisado.
        """
        searchExistsContactAndOpen(self, contato)

    def abrir_conversa_por_nome(self, contato):
        """
        Abre diretamente a conversa com o nome do contato.

        Args:
            contato (str): Nome do contato.
        """
        abrir_conversa_por_nome(self, contato)
