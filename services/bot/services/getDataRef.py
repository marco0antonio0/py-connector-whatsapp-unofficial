import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation



def getDataRef(self:"automation"):
    try:
        # Verifica se o QR code expirou
        try:
            elementoDeRecarregamentoDaPagina = self.driver.find_element(
                By.XPATH, '//div[text()="Clique para recarregar o QR code"]'
            )
            if elementoDeRecarregamentoDaPagina:
                # print("[DEBUG] QR code expirado. Recarregando a página...")
                self.driver.get(self.site)
                time.sleep(2)  # tempo para garantir que o reload seja processado
                return None
        except NoSuchElementException:
            pass  # QR ainda está válido

        # Procura o canvas com o QR code
        canvas_QRCode = self.driver.find_element(
            By.XPATH, '//canvas[@aria-label="Scan this QR code to link a device!"]'
        )
        # print("[DEBUG] Canvas do QR code encontrado.")

        # Acessa o ancestral com o atributo 'data-ref'
        parent = canvas_QRCode.find_element(By.XPATH, "./ancestor::div[@data-ref]")
        data_ref = parent.get_attribute("data-ref")
        # print(f"[DEBUG] data-ref extraído: {data_ref}")
        return data_ref

    except NoSuchElementException:
        # print("[DEBUG] QR code ou elemento necessário não encontrado.")
        return None
    except Exception as e:
        # print(f"[DEBUG] Erro inesperado ao obter o data-ref: {e}")
        return None
