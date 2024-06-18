from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from generateQRcode import createQRCODE
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from PIL import Image


class automation:
    def __init__(self, gui=False):
        self.loginStatus = False
        # point setters de site
        self.site = "https://web.whatsapp.com/"
        # configuração do drive para persistir dados de sessão
        # Configurar as opções do ChromeDriver
        opt = Options()
        if gui is not True:
            opt.add_argument("--headless=new")
            opt.add_argument("--disable-gpu")
            opt.add_argument("--no-sandbox")
            opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("lang=pt-br")
        opt.add_argument("user-data-dir=dados")
        opt.add_argument("start-maximized")

        # Inicializar o ChromeDriver com as opções configuradas
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=opt
        )

    # inicia o projeto
    # requisito: []
    # objetivo:
    # direciona a abrir o site
    # retorno:
    # []
    def getDataRef(self):
        try:
            # Procura pelo elemento com a classe '_akau' que contém o atributo 'data-ref'
            element = self.driver.find_element(
                By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div'
            )

            # Captura o valor do atributo 'data-ref'
            data_ref = element.get_attribute("data-ref")
            return data_ref
        except:
            return None

    def login(self):
        try:
            text = self.getDataRef()
            if type(text) == type(""):
                if len(text) > 0:
                    # Se o botão de novas conversas for encontrado, clique nele e saia do loop
                    print("======================================================")
                    createQRCODE(text)
                    print("======================================================")
                    print("QRCODE criado com sucesso")
                    print("QRCODE valido por 2 minutos")
                    print("1.scane o qrcode do whatsapp")
                    print(
                        "2.Ao realizar o login do whatsapp aguarde o tempo de 2 minutos para o progama starta"
                    )
                    print("======================================================")
                    print("  Verificando crendenciais")
                    print("=============================")
                    time.sleep(2 * 60)
                    self.driver.get(self.site)
                    return True

                return False
            return False

        except NoSuchElementException:
            # Se o botão de novas conversas não for encontrado, espere 1 segundo e tente novamente
            time.sleep(10)
            return False

    def checkIsLogin(self):
        try:
            # Encontre o elemento div com a classe "_ah_-"
            div_element = self.driver.find_element(By.CSS_SELECTOR, "div._ah_-")
            # Extraia o texto contido dentro do elemento
            texto = div_element.text
            if type(texto) == type(""):
                if len(texto) > 0:
                    return True
                return False
            return False
        except:
            return False

    def start(self):
        print("\n")
        print("=============================")
        print("     Iniciando sistema")
        print("=============================")
        self.driver.get(self.site)
        print("  Verificando crendenciais")
        print("=============================")
        while self.loginStatus is not True:
            if self.checkIsLogin():
                self.loginStatus = True
            self.login()

    # requisito: []
    # objetivo:
    # direciona a abrir o site
    # retorno:
    def go_to_home(self):
        # Enviar a tecla ESC para sair da conversa
        temp = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p",
        )
        temp.send_keys(Keys.ESCAPE)  # Simula tecla esc

    # requisito: []
    # objetivo:
    # procura o contato pela barra de pesquisa e deixa na tela de conversa com o contato desejado
    # retorno:
    # []
    def openChatByContact(self, contato):
        # Esperar até que o botão de novas conversas esteja disponível
        while True:
            try:
                button_NewChat = self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span",
                )
                # Se o botão de novas conversas for encontrado, clique nele e saia do loop
                button_NewChat.click()
                break
            except NoSuchElementException:
                # Se o botão de novas conversas não for encontrado, espere 1 segundo e tente novamente
                time.sleep(1)

        # tempo de espera de 1 segundos
        time.sleep(1)

        # Seleciona o campo de pesquisa
        campo_de_pesquisa = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]/p",
        )

        # Envia o nome do contato para o campo de pesquisa
        campo_de_pesquisa.send_keys(contato)

        # tempo de espera de 3 segundos
        time.sleep(3)

        # Seleciona a lista de contatos
        lista_de_contatos = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div/div",
        )

        # Encontra o contato específico "Marco Antonio" na lista de contatos
        contato_marco = lista_de_contatos.find_element(
            By.XPATH, f".//*[text()='{contato}']"
        )

        # Clica no contato "Marco Antonio" para iniciar a conversa
        contato_marco.click()

    # requisito:
    # progama precisa estar em funcionamento
    # objetivo:
    # cola uma imagem no campo de mensagem e pressiona Enter para envia-la
    # parâmetros:
    # - image_path: caminho da imagem a ser enviada
    # retorno:
    # -
    def openImage(self, image_path):
        try:
            # Abre a imagem
            image = Image.open(image_path)
            return image
        except FileNotFoundError:
            print("Arquivo não encontrado.")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao abrir a imagem: {e}")
            return None

    def sendFigure(self, midia):
        attach = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        attach.send_keys(midia)
        while True:
            try:
                self.driver.find_element(
                    By.CSS_SELECTOR, "span[data-icon='send'][class='xsgj6o6']"
                ).click()
                break
            except:
                pass

    def sendImageWithText(self, midia, text):
        campo_de_pesquisa_chat = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p",
        )
        for message in text.split("\n"):
            campo_de_pesquisa_chat.send_keys(message)
            # time.sleep(1)
            campo_de_pesquisa_chat.send_keys(
                Keys.SHIFT + Keys.ENTER
            )  # Simula uma quebra de linha
        time.sleep(3)
        self.driver.find_element(
            By.CSS_SELECTOR, "span[data-icon='attach-menu-plus']"
        ).click()
        attach = self.driver.find_element(
            By.CSS_SELECTOR, "input[type='file'][accept*='image'][accept*='video']"
        )
        attach.send_keys(midia)
        while True:
            try:
                self.driver.find_element(
                    By.CSS_SELECTOR, "span[data-icon='send'][class='xsgj6o6']"
                ).click()
                break
            except:
                pass

    # requisito:
    # é necessario ja ter executado o 'openChatByContact' na fase anterior
    # objetivo:
    # envia a mnsagem para o usuario
    # retorno:
    # []
    def sendMensage(self, text):
        campo_de_pesquisa_chat = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p",
        )
        for message in text.split("\n"):
            campo_de_pesquisa_chat.send_keys(message)
            campo_de_pesquisa_chat.send_keys(Keys.SHIFT + Keys.ENTER)
        time.sleep(1)

        campo_de_pesquisa_chat.send_keys(Keys.ENTER)

    def sendMensageWithTab(self, text):
        campo_de_pesquisa_chat = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p",
        )
        campo_de_pesquisa_chat.send_keys(text)

        time.sleep(1)
        campo_de_pesquisa_chat.send_keys(Keys.TAB)
        time.sleep(1)
        campo_de_pesquisa_chat.send_keys(Keys.ENTER)

    # requisito:
    # progama precisa esta em funcionamento
    # objetivo:
    # encerra o progama
    # returno:
    # []
    def exit(self):
        # fecha o app
        self.driver.quit()

    # requisito:
    # precisa esta na pagina inicial
    # objetivo:
    # procura notificação de nova mensagem e clica no usuario correspondente
    # retorno:
    # retorna o valor do titulo identificador do usuario
    def VerificarNovaMensagem(self):
        while True:
            try:
                # Encontra todos os elementos com a classe "_ahlk"
                elements = self.driver.find_elements(By.XPATH, "//*[@class='_ahlk']")

                # Verifica cada elemento e clica no container pai
                for element in elements:

                    # Clica no container pai do elemento atual
                    container = element.find_element(By.XPATH, "./..")

                    # Seleciona o elemento pai
                    container.click()

                # Encontrar o elemento TITULO span pelo XPath fornecido
                span_element = self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div/div/div/span",
                )
                # Obter o texto do elemento span
                mensagem = span_element.text
                return mensagem  # Retorna a mensagem se houver uma nova

            except NoSuchElementException:
                # Se nenhum elemento com a classe "_ahlk" for encontrado, continue o loop
                pass

            # Verificar a cada segundo
            time.sleep(1)

    # requisito:
    # precisa esta na conversa do contato
    # objetivo:
    # captura a ultima mensagem do contato e guarda ela no array de dados de retorno
    # retorno:
    # retorna a string da mensagem
    def pegar_ultima_mensagem(self):
        try:
            # Encontra o elemento que contém a lista de mensagens
            lista_mensagens_element = self.driver.find_element(
                By.XPATH,
                '//*[@id="main"]/div[3]',
            )

            # Encontra todos os elementos de mensagem dentro da lista
            mensagens = lista_mensagens_element.find_elements(
                By.XPATH, ".//div[contains(@class, 'message-in')]"
            )

            # Se houver mensagens na lista
            if mensagens:
                # Tentar isolar apenas o texto da mensagem, ignorando o horário
                # Supõe-se que a mensagem e o horário estejam em elementos separados dentro de cada 'message-in'
                texto_da_mensagem = (
                    mensagens[-1]
                    .find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]")
                    .text
                )

                # Separação de texto e horário caso estejam no mesmo elemento
                partes_do_texto = texto_da_mensagem.split("\n")
                if len(partes_do_texto) > 1:
                    return " ".join(
                        partes_do_texto[:-1]
                    )  # Ignora a última parte assumindo que é o horário
                else:
                    return texto_da_mensagem  # Retorna o texto como está se não conseguir dividir

        except Exception as e:
            print(f"Erro ao pegar a última mensagem: {e}")
            return "Erro ao encontrar a mensagem"

        return "Nenhuma mensagem encontrada"

    def searchExistsContactAndSendMessage(self, titulo_contato, text):
        try:
            # Encontrar a lista de conversas
            lista_de_conversas = self.driver.find_element(
                By.CSS_SELECTOR, "div[aria-label='Lista de conversas']"
            )
            # Procurar o contato com o título fornecido
            contato = lista_de_conversas.find_element(
                By.XPATH, f".//span[@title='{titulo_contato}']"
            )
            # Clicar no contato encontrado
            contato.click()
            # Enviar a mensagem após abrir a conversa
            self.sendMensage(text=text)
            time.sleep(1)

        except NoSuchElementException:
            print(f"Error: Contato '{titulo_contato}' não encontrado.")
