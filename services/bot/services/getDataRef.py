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

        # Estratégia robusta: encontra qualquer container do QR com data-ref,
        # sem depender de idioma/aria-label.
        candidates = self.driver.find_elements(
            By.XPATH, '//div[@data-ref and .//canvas]'
        )
        for parent in candidates:
            data_ref = (parent.get_attribute("data-ref") or "").strip()
            if data_ref:
                return data_ref

        # Fallback legado por aria-label contendo "QR".
        canvas_qr = self.driver.find_element(
            By.XPATH, '//canvas[contains(@aria-label, "QR")]'
        )
        parent = canvas_qr.find_element(By.XPATH, "./ancestor::div[@data-ref]")
        return (parent.get_attribute("data-ref") or "").strip() or None

    except NoSuchElementException:
        return None
    except Exception:
        return None
