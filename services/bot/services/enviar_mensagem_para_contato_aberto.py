from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def enviar_mensagem_para_contato_aberto(self: "automation", texto: str):
    try:
        print(f"✉️ Enviando mensagem: {texto}")

        campo_mensagem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p'
            ))
        )

        actions = ActionChains(self.driver)
        actions.move_to_element(campo_mensagem)
        actions.click()
        actions.send_keys(texto)
        actions.send_keys(Keys.ENTER)
        actions.perform()

        print("✅ Mensagem enviada com sucesso!")
        time.sleep(2)
        return True

    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return True
