from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation

def sendFigure(self: "automation", midia: str):
    try:
        if not os.path.isfile(midia):
            return False

        button_plus = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="main"]//footer//button['
                '@aria-label or @title or .//span[@data-icon="plus"]'
                ']',
            ))
        )
        button_plus.click()
        time.sleep(0.7)

        image_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[@id='app']//input[@type='file' and "
                "(contains(@accept,'image') or contains(@accept,'video'))]"
            ))
        )

        abs_path = os.path.abspath(midia)
        image_input.send_keys(abs_path)

    except Exception:
        return False

    try:
        time.sleep(1.5)
        send_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        send_button.click()
        time.sleep(1.5)
        return True
    except Exception:
        return False
