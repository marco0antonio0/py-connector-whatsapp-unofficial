from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def go_to_home(self:"automation"):
    try:
        # print("🏠 Tentando voltar para a tela inicial (pressionando ESC)...")
        # body = self.driver.find_element(By.TAG_NAME, "body")
        # body.send_keys(Keys.ESCAPE)
        # print("✅ Tecla ESC pressionada com sucesso.")
        self.driver.get(self.site)
    except Exception as e:
        # print(f"❌ Erro ao tentar ir para a home: {e}")
        pass