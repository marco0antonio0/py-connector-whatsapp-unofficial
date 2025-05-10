from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation

def start_api(self: "automation"):
    print("\n")
    print("======================================================")
    print("                Iniciando sistema")
    print("======================================================")
    self.driver.get(self.site)
    print("               Startado o sistema")
    print("======================================================")
