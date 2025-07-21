from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def pegar_ultima_mensagem(self: "automation") -> str:
    try:
        # Tenta encontrar todas as mensagens recebidas (message-in)
        mensagens = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'message-in')]"
        )

        if not mensagens:
            return "Nenhuma mensagem encontrada"

        ultima = mensagens[-1]

        # Busca o texto da última mensagem
        texto_elemento = ultima.find_element(
            By.XPATH,
            ".//div[contains(@class, 'copyable-text')]"
        )
        texto = texto_elemento.text.strip()

        # Remove horário se houver
        partes = texto.split("\n")
        mensagem_final = " ".join(partes[:-1]) if len(partes) > 1 else texto

        return mensagem_final

    except Exception as e:
        return f"Erro ao encontrar a mensagem: {str(e)}"
