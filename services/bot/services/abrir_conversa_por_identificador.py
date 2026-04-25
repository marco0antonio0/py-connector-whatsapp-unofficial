import re
from typing import TYPE_CHECKING
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if TYPE_CHECKING:
    from ..bot import automation


def _only_digits(value: str) -> str:
    return re.sub(r"\D+", "", value or "")


def _wait_chat_ready(self: "automation", timeout: int = 12) -> bool:
    selectors = [
        (By.XPATH, '//*[@id="main"]//*[@data-testid="conversation-compose-box-input"]'),
        (By.XPATH, '//*[@id="main"]//footer//div[@role="textbox" and @contenteditable="true"]'),
        (By.XPATH, '//*[@id="main"]//div[@role="textbox" and @contenteditable="true"]'),
    ]
    for by, selector in selectors:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return True
        except Exception:
            continue
    return False


def _abrir_por_numero_url(self: "automation", digits: str) -> bool:
    if not digits:
        return False
    self.driver.get(f"https://web.whatsapp.com/send?phone={digits}&text&app_absent=0")
    return _wait_chat_ready(self, timeout=15)


def abrir_conversa_por_identificador(self: "automation", identificador: str) -> bool:
    info = self.identificar_contato(identificador)
    if info.get("tipo") == "invalido":
        return False

    # Estratégia 1: para numero/jid, abre direto por URL (mais estável que busca textual)
    numero_digits = _only_digits((info.get("numero") or ""))
    if numero_digits and _abrir_por_numero_url(self, numero_digits):
        return True

    if info.get("jid"):
        jid_user = _only_digits(str(info["jid"]).split("@", 1)[0])
        if jid_user and _abrir_por_numero_url(self, jid_user):
            return True

    candidates = []
    for key in ("nome", "numero", "jid", "lid", "input"):
        value = (info.get(key) or "").strip()
        if value and value not in candidates:
            candidates.append(value)

    # Para jid/lid, também tenta user-part numérico como fallback de busca
    for key in ("jid", "lid"):
        value = (info.get(key) or "").strip()
        if value and "@" in value:
            user = value.split("@", 1)[0]
            user_digits = _only_digits(user)
            if user_digits and user_digits not in candidates:
                candidates.append(user_digits)

    for candidate in candidates:
        if self.searchExistsContactAndOpen(candidate):
            return True
    return False
