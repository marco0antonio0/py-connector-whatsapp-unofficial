from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def checkIsLogin(self:"automation"):
    try:
        # print("[DEBUG] Verificando se o login foi realizado...")

        # Tenta encontrar o elemento <p> dentro da sidebar de contatos
        login_element = self.driver.find_element(
            By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p'
        )

        # print("[DEBUG] Elemento de login encontrado com sucesso.")
        # Verifica se é um <p> vazio (o padrão que aparece após o login)
        if login_element.tag_name == "p":
            # print("[DEBUG] Tag <p> confirmada. Login presumido com sucesso.")
            return True
        else:
            # print("[DEBUG] Elemento não é uma tag <p>. Login não detectado.")
            return False

    except Exception as e:
        # print(f"[DEBUG] Exceção ao verificar login: {e}")
        return False