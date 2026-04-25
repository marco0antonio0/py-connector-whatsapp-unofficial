from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import psutil
import subprocess
from typing import Callable, Dict, List

from .services.getDataRef import getDataRef
from .services.login import login
from .services.checkIsLogin import checkIsLogin
from .services.start import start
from .services.start_api import start_api
from .services.go_to_home import go_to_home
from .services.openImage import openImage
from .services.searchExistsContactAndOpen import searchExistsContactAndOpen
from .services.pegar_ultima_mensagem import pegar_ultima_mensagem
from .services.pegar_todas_mensagens import pegar_todas_mensagens
from .services.VerificarNovaMensagem import VerificarNovaMensagem
from .services.enviar_mensagem_para_contato_aberto import enviar_mensagem_para_contato_aberto
from .services.sendFigure import sendFigure
from .services.abrir_conversa_por_nome import abrir_conversa_por_nome


class automation:
    """Automação do WhatsApp Web via Selenium."""

    def __init__(self, gui: bool = False):
        self.loginStatus = False
        self._ready_emitted = False
        self._bridge_installed = False
        self._events: Dict[str, List[Callable[[dict], None]]] = {}
        self.site = "https://web.whatsapp.com/"
        self.user_data_dir = os.path.abspath("dados")
        devtools_path = os.path.join(self.user_data_dir, "DevToolsActivePort")

        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    if proc.info['cmdline'] and any(self.user_data_dir in str(arg) for arg in proc.info['cmdline']):
                        subprocess.run(["pkill", "-f", "chrome"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        if os.path.exists(devtools_path):
            try:
                os.remove(devtools_path)
            except OSError:
                pass

        opt = Options()
        if not gui:
            opt.add_argument("--headless=new")
            opt.add_argument("--disable-gpu")
            opt.add_argument("--no-sandbox")
            opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("lang=pt-br")
        opt.add_argument("start-maximized")
        opt.add_argument(f"user-data-dir={self.user_data_dir}")

        driver_path = os.path.abspath("chromeDrive/chromedriver")
        self.driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=opt)

    def on(self, event_name: str, callback: Callable[[dict], None]):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    def emit(self, event_name: str, payload: dict | None = None):
        payload = payload or {}
        for callback in self._events.get(event_name, []):
            try:
                callback(payload)
            except Exception as e:
                print(f"[event:{event_name}] erro no callback: {e}")

    def _install_dom_event_bridge(self):
        script = r"""
            if (!window.__pywaEvents) window.__pywaEvents = [];
            if (window.__pywaBridgeInstalled) return true;

            const pushEvent = (type, payload) => {
                window.__pywaEvents.push({ type, payload, ts: Date.now() });
            };

            const getUnreadContacts = () => {
                const grid = document.querySelector('div[role="grid"][aria-label*="Lista de conversas"]');
                if (!grid) return [];

                const rows = grid.querySelectorAll('div[role="row"]');
                const names = [];
                rows.forEach((row) => {
                    const hasUnread = !!row.querySelector('span[data-testid="icon-unread-count"]');
                    if (!hasUnread) return;

                    const nameEl = row.querySelector(
                        'div[role="gridcell"][aria-colindex="2"] span[dir="auto"][title]'
                    );
                    const name = nameEl && nameEl.getAttribute('title')
                        ? nameEl.getAttribute('title').trim()
                        : '';
                    if (name) names.push(name);
                });
                names.sort();
                return names;
            };

            const emitUnreadDiff = () => {
                const current = getUnreadContacts();
                const prev = window.__pywaLastUnread || [];

                const prevSet = new Set(prev);
                current.forEach((contact) => {
                    if (!prevSet.has(contact)) {
                        pushEvent('unread_added', { contact });
                    }
                });

                if (JSON.stringify(prev) !== JSON.stringify(current)) {
                    pushEvent('unread_snapshot', { contacts: current });
                }

                window.__pywaLastUnread = current;
            };

            const paneSide = document.querySelector('#pane-side');
            if (paneSide) {
                const observer = new MutationObserver(() => emitUnreadDiff());
                observer.observe(paneSide, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    characterData: true
                });
                window.__pywaObserver = observer;
            }

            emitUnreadDiff();
            pushEvent('bridge_ready', {});
            window.__pywaBridgeInstalled = true;
            return true;
        """
        self.driver.execute_script(script)
        self._bridge_installed = True

    def pump_events(self) -> int:
        if not self._bridge_installed:
            try:
                self._install_dom_event_bridge()
            except Exception:
                return 0

        raw_events: List[dict] = self.driver.execute_script(
            "const ev = window.__pywaEvents || []; window.__pywaEvents = []; return ev;"
        )
        if not raw_events:
            return 0

        for event in raw_events:
            event_type = event.get("type", "")
            payload = event.get("payload", {}) or {}

            # Compatibilidade com nomenclatura de evento comum do wwebjs
            if event_type == "unread_added":
                self.emit("message", payload)

            self.emit(event_type, payload)

        return len(raw_events)

    def getDataRef(self):
        return getDataRef(self)

    def login(self, timeout_seconds: int = 180):
        return login(self, timeout_seconds=timeout_seconds)

    def checkIsLogin(self):
        return checkIsLogin(self)

    def start(self):
        start(self)
        if self.loginStatus and not self._ready_emitted:
            try:
                self._install_dom_event_bridge()
            except Exception as e:
                print(f"[evento] ponte DOM não instalada: {e}")
            self.emit("ready", {"status": "ready"})
            self._ready_emitted = True

    def start_api(self):
        start_api(self)

    def go_to_home(self):
        return go_to_home(self)

    def openImage(self, image_path: str):
        return openImage(self, image_path)

    def sendFigure(self, midia):
        return sendFigure(self, midia)

    def enviar_mensagem_para_contato_aberto(self, texto: str) -> bool:
        return enviar_mensagem_para_contato_aberto(self, texto)

    def exit(self):
        self.driver.quit()

    def VerificarNovaMensagem(self) -> list:
        return VerificarNovaMensagem(self)

    def pegar_ultima_mensagem(self):
        return pegar_ultima_mensagem(self)

    def pegar_todas_mensagens(self):
        return pegar_todas_mensagens(self)

    def searchExistsContactAndOpen(self, contato: str):
        return searchExistsContactAndOpen(self, contato)

    def abrir_conversa_por_nome(self, contato: str):
        return abrir_conversa_por_nome(self, contato)
