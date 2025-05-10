from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation

def sendFigure(self: "automation", midia: str):
    # print("📎 Preparando envio de imagem...")

    try:
        # Clica no botão de anexos
        button_plus = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button'
            ))
        )
        button_plus.click()
        time.sleep(1)

        # Seleciona especificamente o input com accept=image/*
        image_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[@id='app']//input[@type='file' and contains(@accept,'image')]"
            ))
        )

        if not os.path.isfile(midia):
            # print(f"❌ Arquivo não encontrado: {midia}")
            return

        abs_path = os.path.abspath(midia)
        # print(f"📁 Enviando mídia: {abs_path}")
        image_input.send_keys(abs_path)

    except Exception as e:
        # print(f"❌ Erro ao selecionar input correto de imagem: {e}")
        return

    # print("⏳ Aguardando botão de envio ficar disponível...")

    try:
        # Aguarda pré-visualização e clica em "enviar"
        time.sleep(3)
        send_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        send_button.click()
        time.sleep(4)
        # print("✅ Mídia enviada com sucesso!")
    except Exception as e:
        # print(f"❌ Erro ao clicar no botão de envio: {e}")
        pass
