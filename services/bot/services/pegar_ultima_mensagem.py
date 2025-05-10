from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def pegar_ultima_mensagem(self:"automation"):
    try:
        # print("🔍 Buscando o elemento da lista de mensagens...")
        lista_mensagens_element = self.driver.find_element(
            By.XPATH,
            '//*[@id="main"]/div[3]/div/div[2]/div[3]',
        )
        # print("✅ Elemento da lista de mensagens encontrado.")

        # print("🔍 Buscando todas as mensagens recebidas (message-in)...")
        mensagens = lista_mensagens_element.find_elements(
            By.XPATH, ".//div[contains(@class, 'message-in')]"
        )
        # print(f"📨 Total de mensagens encontradas: {len(mensagens)}")

        if mensagens:
            # print("📥 Pegando a última mensagem da lista...")
            ultima_mensagem = mensagens[-1]

            # print("🔍 Buscando o texto da última mensagem...")
            texto_da_mensagem = ultima_mensagem.find_element(
                By.XPATH, ".//div[contains(@class, 'copyable-text')]"
            ).text
            # print(f"📝 Texto bruto da mensagem: {texto_da_mensagem}")

            partes_do_texto = texto_da_mensagem.split("\n")
            # print(f"🔎 Partes do texto separadas: {partes_do_texto}")

            if len(partes_do_texto) > 1:
                mensagem_final = " ".join(partes_do_texto[:-1])
                # print(f"✅ Mensagem final sem horário: {mensagem_final}")
                return mensagem_final
            else:
                # print(f"✅ Mensagem final (sem separação detectada): {texto_da_mensagem}")
                return texto_da_mensagem

    except Exception as e:
        # print(f"❌ Erro ao pegar a última mensagem: {e}")
        return "Erro ao encontrar a mensagem"

    # print("⚠️ Nenhuma mensagem encontrada.")
    return "Nenhuma mensagem encontrada"