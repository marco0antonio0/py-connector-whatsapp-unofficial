import segno

def createQRCODE(text):
    try:
        qr = segno.make(text, error='L')
        qr.terminal(compact=True, border=1)
    except Exception as e:
        print(f"Erro ao gerar QR code: {e}")
