from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import psutil
import subprocess
import threading
import time
from typing import Callable, Dict, List, Optional, Set

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


class _NewMessageHook:
    """
    Hook de nova mensagem no estilo decorator.
    Uso:
        @instance.hook_new_message()
        def callback(payload):
            contato = instance.hook_new_message.contato
            ...
    """

    def __init__(self, owner: "automation"):
        self._owner = owner
        self.contato: str = ""

    def __call__(self):
        def decorator(func: Callable):
            self._owner._hook_new_message_handler = func
            return func
        return decorator


class automation:
    """Automação do WhatsApp Web via Selenium."""

    def __init__(self, gui: bool = False):
        self.loginStatus = False
        self._ready_emitted = False
        self._bridge_installed = False
        self._events: Dict[str, List[Callable[[dict], None]]] = {}
        self._hook_new_message_handler: Optional[Callable] = None
        self.hook_new_message = _NewMessageHook(self)
        self._background_running = False
        self._background_thread: Optional[threading.Thread] = None
        self._known_unread: Set[str] = set()
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
        self.on("message", self._handle_message_hook)
        self.on("unread_snapshot", self._handle_unread_snapshot)

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

    def _handle_unread_snapshot(self, payload: dict):
        contatos = payload.get("contacts", [])
        if not isinstance(contatos, list):
            return
        self._known_unread = {c.strip() for c in contatos if isinstance(c, str) and c.strip()}

    def _handle_message_hook(self, payload: dict):
        contato = (payload.get("contact") or "").strip()
        if not contato:
            return
        self.hook_new_message.contato = contato

        if self._hook_new_message_handler is None:
            return

        try:
            # Prioriza assinatura callback(payload)
            self._hook_new_message_handler(payload)
        except TypeError:
            # Compatibilidade: callback() sem argumentos
            self._hook_new_message_handler()
        except Exception as e:
            print(f"[hook_new_message] erro no callback: {e}")

    def _background_loop(self, poll_interval: float, fallback_interval: float):
        last_fallback = 0.0
        while self._background_running:
            try:
                self.pump_events()
            except Exception as e:
                print(f"[background] erro no pump_events: {e}")

            now = time.time()
            if now - last_fallback >= fallback_interval:
                last_fallback = now
                try:
                    unread_now = {c for c in self.VerificarNovaMensagem() if isinstance(c, str) and c.strip()}
                    novos = unread_now - self._known_unread
                    for contato in sorted(novos):
                        self.emit("message", {"contact": contato, "source": "fallback"})
                    self._known_unread = unread_now
                except Exception as e:
                    print(f"[background] erro no fallback unread: {e}")

            time.sleep(max(0.2, poll_interval))

    def start_background(self, poll_interval: float = 1.0, fallback_interval: float = 3.0):
        if self._background_running:
            return
        self._background_running = True
        self._background_thread = threading.Thread(
            target=self._background_loop,
            args=(poll_interval, fallback_interval),
            daemon=True,
            name="pywa-event-loop",
        )
        self._background_thread.start()

    def stop_background(self):
        self._background_running = False
        if self._background_thread and self._background_thread.is_alive():
            self._background_thread.join(timeout=2.0)

    def run(self, poll_interval: float = 1.0, fallback_interval: float = 3.0, block: bool = True):
        """
        Decorator para iniciar o loop em background.
        Uso:
            @instance.run()
            @instance.hook_new_message()
            def callback(payload):
                ...
        """

        def decorator(func: Callable):
            self.start_background(poll_interval=poll_interval, fallback_interval=fallback_interval)

            if block:
                try:
                    while self._background_running:
                        time.sleep(0.5)
                except KeyboardInterrupt:
                    self.stop_background()
            return func

        return decorator

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
        self.stop_background()
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
