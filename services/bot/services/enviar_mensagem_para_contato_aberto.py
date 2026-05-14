import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import TYPE_CHECKING
import traceback

if TYPE_CHECKING:
    from ..bot import automation


def _normalize_for_chromedriver(texto: str) -> str:
    # Evita erro "ChromeDriver only supports characters in the BMP".
    # Remove caracteres fora de U+0000..U+FFFF (ex.: alguns emojis).
    return "".join(ch for ch in str(texto) if ord(ch) <= 0xFFFF)


def enviar_mensagem_para_contato_aberto(self: "automation", texto: str):
    try:
        texto = _normalize_for_chromedriver(texto)
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
                '//*[@id="main"]//footer//p|//*[@id="main"]//div[@contenteditable="true"]//p',
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

        try:
            campo_mensagem.click()

            # Preserva quebras de linha no WhatsApp:
            # usa Shift+Enter entre linhas e Enter apenas ao final para enviar.
            linhas = str(texto).split("\n")
            for idx, linha in enumerate(linhas):
                if linha:
                    campo_mensagem.send_keys(linha)
                if idx < len(linhas) - 1:
                    campo_mensagem.send_keys(Keys.SHIFT + Keys.ENTER)

            campo_mensagem.send_keys(Keys.ENTER)
        except Exception:
            # Fallback para composer contenteditable quando send_keys falha em <p>
            self.driver.execute_script(
                """
                const el = arguments[0];
                const text = arguments[1];
                el.focus();
                if (el.isContentEditable) {
                  el.textContent = text;
                } else {
                  el.value = text;
                }
                """,
                campo_mensagem,
                texto,
            )
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()

        print("✅ Mensagem enviada com sucesso!")
        time.sleep(1)
        return True

    except Exception as e:
        print(f"❌ Erro ao enviar mensagem ({type(e).__name__}): {e}")
        traceback.print_exc()
        return False
