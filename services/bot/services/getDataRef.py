import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation



def getDataRef(self:"automation"):
    try:
        # Verifica se o QR code expirou
        try:
            elementoDeRecarregamentoDaPagina = self.driver.find_element(
                By.XPATH,
                '//div[contains(translate(text(),'
                '"ABCDEFGHIJKLMNOPQRSTUVWXYZ",'
                '"abcdefghijklmnopqrstuvwxyz"),"recarregar o qr code")]',
            )
            if elementoDeRecarregamentoDaPagina:
                self.driver.get(self.site)
                time.sleep(2)
                return None
        except NoSuchElementException:
            pass

        # Procura o canvas do QR code sem depender de idioma exato do aria-label
        canvas_QRCode = self.driver.find_element(
            By.XPATH, '//canvas[contains(@aria-label, "QR")]'
        )

        parent = canvas_QRCode.find_element(By.XPATH, "./ancestor::div[@data-ref]")
        data_ref = parent.get_attribute("data-ref")
        return data_ref

    except NoSuchElementException:
        return None
    except Exception:
        return None
