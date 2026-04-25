from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def enviar_mensagem_por_identificador(self: "automation", identificador: str, texto: str) -> bool:
    abriu = self.abrir_conversa_por_identificador(identificador)
    if not abriu:
        return False
    return self.enviar_mensagem_para_contato_aberto(texto)

