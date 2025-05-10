from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..bot import automation

def VerificarNovaMensagem(self: "automation") -> List[str]:
    nomes_com_nova_mensagem = []

    try:
        elements = self.driver.find_elements(By.XPATH, "//*[@class='_ahlk']")

        for element in elements:
            try:
                # Sobe até o bloco completo da conversa
                bloco_conversa = element.find_element(By.XPATH, "../../../../..")
                
                # Busca o <span> com atributo title dentro do bloco
                nome_element = bloco_conversa.find_element(By.XPATH, ".//span[@title]")
                nome = nome_element.get_attribute("title").strip()

                if nome:
                    nomes_com_nova_mensagem.append(nome)
                else:
                    nomes_com_nova_mensagem.append("[Nome vazio]")

            except Exception as e:
                print(f"[Erro ao obter nome]: {e}")
                nomes_com_nova_mensagem.append("[Erro ao obter nome]")

    except NoSuchElementException:
        pass

    except Exception as e:
        print(f"[Erro inesperado] {e}")

    return nomes_com_nova_mensagem
