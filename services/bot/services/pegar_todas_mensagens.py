from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from ..bot import automation


def pegar_todas_mensagens(self: "automation") -> List[Dict[str, str]]:
    mensagens_extraidas = []

    try:
        lista_mensagens_element = self.driver.find_element(
            By.XPATH,
            '//*[@id="main"]/div[3]/div/div[2]/div[3]'
        )

        mensagens = lista_mensagens_element.find_elements(
            By.XPATH, ".//div[contains(@class, 'message-in') or contains(@class, 'message-out')]"
        )

        for mensagem in mensagens:
            try:
                classe = mensagem.get_attribute("class")

                if "message-out" in classe:
                    autor = "bot"
                elif "message-in" in classe:
                    autor = "cliente"
                else:
                    autor = "desconhecido"

                # Extrair o texto da mensagem
                texto_element = mensagem.find_element(
                    By.XPATH, ".//div[contains(@class, 'copyable-text')]"
                )
                texto = texto_element.text

                partes = texto.split("\n")
                texto_final = " ".join(partes[:-1]) if len(partes) > 1 else texto

                mensagens_extraidas.append({
                    "autor": autor,
                    "mensagem": texto_final
                })

            except Exception as e:
                mensagens_extraidas.append({
                    "autor": "desconhecido",
                    "mensagem": "[Erro ao ler mensagem]"
                })

    except Exception as e:
        print(f"❌ Erro ao obter lista de mensagens: {e}")
        return []

    return mensagens_extraidas
