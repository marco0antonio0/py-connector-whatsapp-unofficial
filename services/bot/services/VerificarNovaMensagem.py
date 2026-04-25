from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..bot import automation

def VerificarNovaMensagem(self: "automation") -> List[str]:
    nomes_com_nova_mensagem = []

    try:
        lista_xpath = (
            '//*[@id="pane-side"]//div[@role="grid" and ('
            'contains(@aria-label, "Lista de conversas") or '
            'contains(@aria-label, "Resultados da pesquisa")'
            ')]'
        )

        # Aguarda a lista de conversas ficar disponível antes de varrer as linhas
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, lista_xpath))
        )

        rows = self.driver.find_elements(
            By.XPATH, f"{lista_xpath}//div[@role='row']"
        )

        for row in rows:
            try:
                # Ignora cabeçalhos da busca (Conversas/Mensagens)
                if row.find_elements(By.XPATH, ".//*[@data-testid='section-header']"):
                    continue

                # Só considera a conversa se houver indicador de mensagens não lidas
                unread = row.find_elements(
                    By.XPATH,
                    ".//span[@data-testid='icon-unread-count']",
                )
                if not unread:
                    continue

                # Extrai o nome do contato na célula principal da conversa (aria-colindex=2)
                nomes = row.find_elements(
                    By.XPATH,
                    ".//div[@role='gridcell' and @aria-colindex='2']"
                    "//span[@dir='auto'][@title]",
                )
                if not nomes:
                    continue

                nome = nomes[0].get_attribute("title").strip()

                if nome and nome not in nomes_com_nova_mensagem:
                    nomes_com_nova_mensagem.append(nome)

            except StaleElementReferenceException:
                pass
            except Exception as e:
                print(f"[Erro ao obter nome]: {e}")

    except TimeoutException:
        pass
    except NoSuchElementException:
        pass
    except Exception as e:
        print(f"[Erro inesperado] {e}")

    return nomes_com_nova_mensagem
