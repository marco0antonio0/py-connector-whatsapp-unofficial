from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def go_to_home(self:"automation"):
    try:
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="pane-side"]//div[@role="grid" and contains(@aria-label,"Lista de conversas")]',
            ))
        )
        return True
    except Exception:
        try:
            self.driver.get(self.site)
            WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//*[@id="pane-side"]//div[@role="grid"]',
                ))
            )
            return True
        except Exception:
            return False
