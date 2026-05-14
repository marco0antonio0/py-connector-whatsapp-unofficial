from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import base64
import mimetypes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def _get_composer(self: "automation"):
    composer_selectors = [
        (By.XPATH, "//*[@id='main']//footer//div[@role='textbox' and @contenteditable='true']"),
        (By.CSS_SELECTOR, "#main footer div[role='textbox'][contenteditable='true']"),
        (By.XPATH, "//*[@id='main']//*[@data-testid='conversation-compose-box-input']"),
    ]
    for by, sel in composer_selectors:
        try:
            return WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((by, sel))
            )
        except Exception:
            continue
    return None


def _paste_image_and_enter(self: "automation", abs_path: str) -> bool:
    composer = _get_composer(self)
    if composer is None:
        print("❌ sendFigure: campo de mensagem não encontrado para colar imagem")
        return False

    mime = mimetypes.guess_type(abs_path)[0] or "image/jpeg"
    with open(abs_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    try:
        composer.click()
    except Exception:
        pass

    script = """
        const composer = arguments[0];
        const base64 = arguments[1];
        const mime = arguments[2];

        function b64toUint8Array(b64) {
          const binary = atob(b64);
          const len = binary.length;
          const bytes = new Uint8Array(len);
          for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);
          return bytes;
        }

        const bytes = b64toUint8Array(base64);
        const file = new File([bytes], 'upload', { type: mime });
        const dt = new DataTransfer();
        dt.items.add(file);

        composer.focus();

        let pasted = false;
        try {
          const pasteEvt = new ClipboardEvent('paste', {
            bubbles: true,
            cancelable: true,
            clipboardData: dt
          });
          pasted = composer.dispatchEvent(pasteEvt) || pasted;
        } catch (_) {}

        try {
          const inputEvt = new InputEvent('beforeinput', {
            bubbles: true,
            cancelable: true,
            inputType: 'insertFromPaste',
            dataTransfer: dt
          });
          pasted = composer.dispatchEvent(inputEvt) || pasted;
        } catch (_) {}

        return true;
    """
    try:
        self.driver.execute_script(script, composer, b64, mime)
        time.sleep(2)
        try:
            active = self.driver.switch_to.active_element
            active.send_keys(Keys.ENTER)
        except Exception:
            composer.send_keys(Keys.ENTER)
        time.sleep(1.2)
        # print("✅ sendFigure: imagem colada no composer e enviada com ENTER")
        return True
    except Exception as e:
        print(f"❌ sendFigure: falha ao colar imagem no composer: {e}")
        return False


def _attach_via_menu_and_send(self: "automation", abs_path: str) -> bool:
    try:
        print(f"📎 sendFigure: tentando anexar {abs_path}")

        # 1) Clica no botão "+" (plus-rounded) no footer da conversa.
        plus_selectors = [
            (
                By.XPATH,
                "//*[@id='main']//footer//*[@data-testid='plus-rounded']/ancestor::button[1]",
            ),
            (
                By.XPATH,
                "//*[@id='main']//footer//*[@data-icon='plus-rounded']/ancestor::button[1]",
            ),
            (
                By.XPATH,
                "//*[@id='main']//footer//*[@data-icon='plus']/ancestor::button[1]",
            ),
        ]
        plus_clicked = False
        for by, sel in plus_selectors:
            try:
                plus_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((by, sel))
                )
                plus_btn.click()
                plus_clicked = True
                print("✅ sendFigure: botão plus clicado")
                time.sleep(0.5)
                break
            except Exception:
                continue

        if not plus_clicked:
            print("❌ sendFigure: não consegui clicar no botão plus")
            return False

        # 2) Clica no item "Fotos e vídeos" dentro do menu.
        fotos_selectors = [
            (
                By.XPATH,
                "//*[@role='menuitem' and (@aria-label='Fotos e vídeos' or .//*[contains(text(),'Fotos e vídeos')])]",
            ),
            (
                By.XPATH,
                "//*[@id='app']//button[@aria-label='Fotos e vídeos']",
            ),
            (
                By.XPATH,
                "//*[@id='app']/div/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/button[2]",
            ),
        ]
        fotos_clicked = False
        for by, sel in fotos_selectors:
            try:
                fotos_btn = WebDriverWait(self.driver, 4).until(
                    EC.element_to_be_clickable((by, sel))
                )
                fotos_btn.click()
                fotos_clicked = True
                print("✅ sendFigure: menu 'Fotos e vídeos' clicado")
                time.sleep(0.7)
                break
            except Exception:
                continue

        if not fotos_clicked:
            print("❌ sendFigure: não consegui clicar em 'Fotos e vídeos'")
            return False

        # 2) Tenta múltiplos inputs de arquivo.
        input_selectors = [
            (By.XPATH, "//*[@id='main']//input[@type='file' and contains(@accept,'image')]"),
            (By.XPATH, "//*[@id='app']//input[@type='file' and contains(@accept,'image')]"),
            (By.XPATH, "//*[@id='app']//input[@type='file' and (contains(@accept,'video') or contains(@accept,'*'))]"),
            (By.XPATH, "//*[@id='app']//input[@type='file']"),
        ]

        sent_to_input = False
        last_input_error = None

        for by, sel in input_selectors:
            inputs = self.driver.find_elements(by, sel)
            if not inputs:
                continue
            for idx, image_input in enumerate(inputs):
                try:
                    image_input.send_keys(abs_path)
                    sent_to_input = True
                    print(f"✅ sendFigure: arquivo enviado para input selector={sel} idx={idx}")
                    break
                except Exception as e:
                    last_input_error = e
                    continue
            if sent_to_input:
                break

        if not sent_to_input:
            print(f"❌ sendFigure: não foi possível enviar arquivo para nenhum input. erro={last_input_error}")
            return False

    except Exception:
        print("❌ sendFigure: erro durante etapa de anexo")
        return False

    try:
        time.sleep(2)
        send_button = None
        send_selectors = [
            (By.CSS_SELECTOR, "span[data-icon='send']"),
            (By.XPATH, "//*[@id='app']//*[@data-icon='send']"),
            (By.XPATH, "//*[@id='app']//button[.//*[@data-icon='send']]"),
            (By.XPATH, "//button[contains(@aria-label,'Enviar') or contains(@aria-label,'Send')]"),
            (By.XPATH, "//*[@id='app']//*[@data-testid='compose-btn-send']"),
        ]
        for by, sel in send_selectors:
            try:
                send_button = WebDriverWait(self.driver, 6).until(
                    EC.element_to_be_clickable((by, sel))
                )
                if send_button:
                    break
            except Exception:
                continue

        if send_button is None:
            # Fallback: ENTER costuma enviar a mídia quando o preview está ativo.
            try:
                active = self.driver.switch_to.active_element
                active.send_keys(Keys.ENTER)
                time.sleep(1.5)
                print("⚠️ sendFigure: botão enviar não encontrado, tentei fallback ENTER")
                return True
            except Exception as e:
                print(f"❌ sendFigure: botão enviar não encontrado e fallback ENTER falhou: {e}")
                return False

        send_button.click()
        time.sleep(1.5)
        print("✅ sendFigure: mídia enviada")
        return True
    except Exception as e:
        print(f"❌ sendFigure: erro ao clicar enviar: {e}")
        return False


def sendFigure(self: "automation", midia: str):
    if not os.path.isfile(midia):
        print(f"❌ sendFigure: arquivo não encontrado: {midia}")
        return False

    abs_path = os.path.abspath(midia)

    # Estratégia principal solicitada: colar imagem no campo e dar ENTER.
    if _paste_image_and_enter(self, abs_path):
        return True

    # Fallback para anexo tradicional se colagem falhar.
    return _attach_via_menu_and_send(self, abs_path)
