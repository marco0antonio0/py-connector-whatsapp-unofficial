from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from typing import TYPE_CHECKING
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.normalizarMessages import normalizar
if TYPE_CHECKING:
    from ..bot import automation

def searchExistsContactAndOpen(self: "automation", contato: str) -> bool:
    try:
        contato_normalizado = normalizar(contato)
        grids_xpath = (
            '//*[@id="pane-side"]//div[@role="grid" and ('
            'contains(@aria-label, "Lista de conversas") or '
            'contains(@aria-label, "Resultados da pesquisa")'
            ')]'
        )
        campo_xpath = (
            '//input[@role="textbox" and '
            '@aria-label="Pesquisar ou começar uma nova conversa"]'
        )

        def _clicar_contato_visivel() -> bool:
            rows = self.driver.find_elements(By.XPATH, f"{grids_xpath}//div[@role='row']")
            for row in rows:
                # ignora cabeçalhos de seção da busca ("Conversas", "Mensagens")
                if row.find_elements(By.XPATH, ".//*[@data-testid='section-header']"):
                    continue

                span_nome = row.find_elements(
                    By.XPATH,
                    ".//div[@role='gridcell' and @aria-colindex='2']//span[@dir='auto'][@title]",
                )
                if not span_nome:
                    continue

                titulo = span_nome[0].get_attribute("title")
                titulo = titulo.strip() if titulo else ""
                if not titulo or normalizar(titulo) != contato_normalizado:
                    continue

                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)

                alvos_click = row.find_elements(
                    By.XPATH,
                    ".//*[@data-testid='cell-frame-container' or "
                    "@data-testid='message-yourself-row' or "
                    "starts-with(@data-testid, 'chatlist-message-')]",
                )
                alvo = alvos_click[0] if alvos_click else row

                try:
                    alvo.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", alvo)

                return True
            return False

        WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.XPATH, f"{grids_xpath}//div[@role='row']"))
        )

        # Primeiro tenta clicar sem pesquisar (mais estável quando conversa já está visível)
        if _clicar_contato_visivel():
            return True

        # Fallback: usa busca e tenta novamente
        campo = WebDriverWait(self.driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, campo_xpath))
        )
        campo.click()
        ActionChains(self.driver)\
            .key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)\
            .send_keys(Keys.DELETE)\
            .perform()
        time.sleep(0.3)
        campo = self.driver.find_element(By.XPATH, campo_xpath)
        campo.send_keys(contato)
        time.sleep(1)

        if _clicar_contato_visivel():
            return True

        print(f"⚠️ Contato '{contato}' não encontrado nos resultados da busca.")
        return False

    except TimeoutException as e:
        print(f"❌ Timeout ao buscar contato '{contato}': {e}")
        return False
    except (NoSuchElementException, StaleElementReferenceException) as e:
        print(f"❌ Erro ao buscar ou digitar no campo de pesquisa: {e}")
        return False
