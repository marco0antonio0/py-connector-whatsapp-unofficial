from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.normalizarMessages import normalizar
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import automation

def abrir_conversa_por_nome(self: "automation", contato: str):
    try:
        print(f"🔍 Procurando contato: {contato}")
        contato_normalizado = normalizar(contato)

        # Aguarda o WhatsApp renderizar os resultados da busca
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                '//div[@id="pane-side"]//span[@title]'
            ))
        )

        # Busca todos os contatos visíveis após a pesquisa
        contatos = self.driver.find_elements(
            By.XPATH,
            '//div[@id="pane-side"]//span[@title]'
        )

        for elemento in contatos:
            titulo_original = elemento.get_attribute("title").strip()
            titulo_normalizado = normalizar(titulo_original)

            # print(f"🔎 Comparando com: {titulo_original}")

            if titulo_normalizado == contato_normalizado:
                # print(f"✅ Contato encontrado: {titulo_original} — clicando...")
                container = elemento.find_element(By.XPATH, "./ancestor::div[@role='listitem']")
                container.click()
                return True

        print("⚠️ Contato não encontrado na lista visível.")
        return False

    except Exception as e:
        print(f"❌ Erro ao tentar abrir a conversa: {e}")
        return False
