import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from services.generateQRcode import createQRCODE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def login(self:"automation"):
    try:
        text = self.getDataRef()
        if type(text) == type(""):
            if len(text) > 0:
                # Se o botão de novas conversas for encontrado, clique nele e saia do loop
                print("======================================================")
                createQRCODE(text)
                print("======================================================")
                print("             QRCODE CRIADO com sucesso")
                print("======================================================")
                print("1. Scane o qrcode do whatsapp")
                print("2. Realizar o login do whatsapp aguarde o tempo alguns segundos para o progama inciar")
                print("======================================================")
                print("             Verificando crendenciais")
                print("======================================================")
                while True:
                    lastText = self.getDataRef()
                    time.sleep(2)
                    if lastText != text:
                        print("======================================================")
                        createQRCODE(lastText)
                        print("======================================================")
                        print("            QRCODE ATUALIZADO com sucesso")
                        print("======================================================")
                        print("1. Scane o qrcode do whatsapp")
                        print("2. Realizar o login do whatsapp aguarde o tempo alguns segundos para o progama inciar")
                        print("======================================================")
                        print("             Verificando crendenciais")
                        print("======================================================")
                        text = lastText

    
                    if self.checkIsLogin():
                        return True

            return False

    except NoSuchElementException:
        # Se o botão de novas conversas não for encontrado, espere 1 segundo e tente novamente
        time.sleep(10)
        return False