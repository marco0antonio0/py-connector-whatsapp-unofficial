import time
from selenium.common.exceptions import NoSuchElementException
from services.generateQRcode import createQRCODE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def login(self: "automation", timeout_seconds: int = 180):
    try:
        qr_atual = None
        expiracao = time.time() + max(30, timeout_seconds)
        qrcode_ja_exibido = False

        while time.time() < expiracao:
            if self.checkIsLogin():
                return True

            novo_qr = self.getDataRef()
            if isinstance(novo_qr, str) and novo_qr.strip():
                if novo_qr != qr_atual:
                    qr_atual = novo_qr
                    createQRCODE(qr_atual)

                    status = "QRCODE CRIADO" if not qrcode_ja_exibido else "QRCODE ATUALIZADO"
                    qrcode_ja_exibido = True

                    print("======================================================")
                    print(f"             {status} com sucesso")
                    print("======================================================")
                    print("1. Scane o qrcode do whatsapp")
                    print("2. Realizar o login do whatsapp aguarde o tempo alguns segundos para o progama inciar")
                    print("======================================================")
                    print("             Verificando crendenciais")
                    print("======================================================")

            time.sleep(2)

        return False

    except NoSuchElementException:
        time.sleep(2)
        return False
    except Exception:
        time.sleep(2)
        return False
