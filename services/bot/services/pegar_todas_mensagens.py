from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from ..bot import automation

def pegar_todas_mensagens(self: "automation") -> List[Dict[str, str]]:
    mensagens_extraidas = []

    try:
        mensagens = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'message-in') or contains(@class, 'message-out')]"
        )

        for mensagem in mensagens:
            try:
                classe = mensagem.get_attribute("class")

                autor = (
                    "bot" if "message-out" in classe
                    else "cliente" if "message-in" in classe
                    else "desconhecido"
                )

                texto_element = mensagem.find_element(
                    By.XPATH, ".//div[contains(@class, 'copyable-text')]"
                )
                texto = texto_element.text.strip()

                # Remove o horário da última linha, se houver
                partes = texto.split("\n")
                texto_final = " ".join(partes[:-1]) if len(partes) > 1 else texto

                mensagens_extraidas.append({
                    "autor": autor,
                    "mensagem": texto_final
                })

            except Exception:
                mensagens_extraidas.append({
                    "autor": "desconhecido",
                    "mensagem": "[Erro ao ler mensagem]"
                })

    except Exception as e:
        print(f"❌ Erro ao buscar mensagens: {e}")
        return []

    return mensagens_extraidas
