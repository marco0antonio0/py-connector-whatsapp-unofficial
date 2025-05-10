from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from typing import TYPE_CHECKING
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
if TYPE_CHECKING:
    from ..bot import automation

def searchExistsContactAndOpen(self: "automation", contato: str) -> bool:
    try:
        # Tenta encontrar e limpar o campo
        campo_xpath = '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p'

        campo = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_xpath))
        )

        # Limpa o campo de forma robusta
        campo.click()
        ActionChains(self.driver)\
            .key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)\
            .send_keys(Keys.DELETE)\
            .perform()

        time.sleep(0.5)

        # Rebusca o campo após limpar (previne StaleElement)
        campo = self.driver.find_element(By.XPATH, campo_xpath)
        campo.send_keys(contato)
        time.sleep(1)

        return self.abrir_conversa_por_nome(contato)

    except (NoSuchElementException, StaleElementReferenceException) as e:
        print(f"❌ Erro ao buscar ou digitar no campo de pesquisa: {e}")
        return False
