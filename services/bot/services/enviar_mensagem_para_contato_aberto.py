from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import TYPE_CHECKING
import traceback

if TYPE_CHECKING:
    from ..bot import automation


def enviar_mensagem_para_contato_aberto(self: "automation", texto: str):
    try:
        print(f"✉️ Enviando mensagem: {texto}")

        seletores = [
            (
                By.XPATH,
                '//footer//div[@role="textbox" and @contenteditable="true"]',
            ),
            (
                By.XPATH,
                '//*[@id="main"]//div[@role="textbox" and @contenteditable="true"]',
            ),
            (
                By.XPATH,
                '//*[@id="main"]//*[@data-testid="conversation-compose-box-input"]',
            ),
            (
                By.XPATH,
                '//*[@id="main"]//div[@contenteditable="true" and ('
                'contains(@aria-label, "mensagem") or contains(@aria-label, "message"))]',
            ),
            (
                By.XPATH,
                '//div[@id="main"]//footer//div[@contenteditable="true"]',
            ),
            (
                By.CSS_SELECTOR,
                '#main footer div[role="textbox"][contenteditable="true"]',
            ),
            (
                By.CSS_SELECTOR,
                '#main div[role="textbox"][contenteditable="true"]',
            ),
            (
                By.XPATH,
                '//*[@id="main"]//footer//p',
            ),
        ]

        campo_mensagem = None
        for by, selector in seletores:
            try:
                campo_mensagem = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located((by, selector))
                )
                if campo_mensagem:
                    break
            except TimeoutException:
                continue

        if not campo_mensagem:
            raise TimeoutException("Campo de mensagem não encontrado no rodapé da conversa.")

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
        print(f"❌ Erro ao enviar mensagem ({type(e).__name__}): {e}")
        traceback.print_exc()
        return False
