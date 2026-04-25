from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from ..bot import automation


def ler_conversa_por_identificador(self: "automation", identificador: str) -> List[Dict[str, str]]:
    abriu = self.abrir_conversa_por_identificador(identificador)
    if not abriu:
        return []
    return self.pegar_todas_mensagens()

