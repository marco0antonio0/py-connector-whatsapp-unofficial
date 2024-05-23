import pyqrcode


def createQRCODE(text):
    try:

        # Criar o QR code
        qr_code = pyqrcode.create(text, error="L")

        # Exibir o QR code no terminal
        print(qr_code.terminal(module_color="black", background="white", quiet_zone=4))
    except:
        print("codigo qrcode não encontrado")
