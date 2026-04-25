from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def checkIsLogin(self:"automation"):
    try:
        # print("[DEBUG] Verificando se o login foi realizado...")

        self.driver.find_element(By.XPATH, '//*[@id="pane-side"]/div')
        return True

    except Exception as e:
        # print(f"[DEBUG] Exceção ao verificar login: {e}")
        return False