from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def checkIsLogin(self:"automation"):
    try:
        self.driver.find_element(
            By.XPATH,
            '//*[@id="pane-side"]//div[@role="grid" and contains(@aria-label,"Lista de conversas")]',
        )
        return True

    except Exception:
        return False
