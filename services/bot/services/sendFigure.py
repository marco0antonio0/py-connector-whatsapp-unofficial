from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def sendFigure(self:"automation", midia):
    attach = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    attach.send_keys(midia)
    while True:
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, "span[data-icon='send'][class='xsgj6o6']"
            ).click()
            break
        except:
            pass