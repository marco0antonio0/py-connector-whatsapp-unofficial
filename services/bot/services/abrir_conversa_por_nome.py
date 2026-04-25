from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import automation

def abrir_conversa_por_nome(self: "automation", contato: str):
    try:
        return bool(self.searchExistsContactAndOpen(contato))

    except Exception as e:
        print(f"❌ Erro ao tentar abrir a conversa: {e}")
        return False
