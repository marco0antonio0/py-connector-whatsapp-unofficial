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
    while self.loginStatus is not True:
        if self.checkIsLogin():
            self.loginStatus = True
        self.login()