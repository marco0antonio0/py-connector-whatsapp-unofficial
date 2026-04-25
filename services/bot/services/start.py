from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation

def start(self: "automation"):
    print("\n")
    print("======================================================")
    print("                Iniciando sistema")
    print("======================================================")
    self.driver.get(self.site)
    print("             Verificando crendenciais")
    print("======================================================")

    if self.checkIsLogin():
        self.loginStatus = True
        return

    self.loginStatus = bool(self.login(timeout_seconds=180))
