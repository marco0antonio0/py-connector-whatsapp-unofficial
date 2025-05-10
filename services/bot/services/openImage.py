import os
import tempfile
from PIL import Image
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation

def openImage(self: "automation", image_path: str) -> str | None:
    try:
        # Abre e converte a imagem para RGB (mais compatível)
        image = Image.open(image_path).convert("RGB")

        # Define um caminho com nome fixo para evitar problemas
        temp_path = os.path.join(tempfile.gettempdir(), "imagem.png")
        image.save(temp_path, format="PNG")

        # print(f"🖼️ Imagem processada e salva em: {temp_path}")
        return temp_path
    except FileNotFoundError:
        # print("❌ Arquivo não encontrado.")
        return None
    except Exception as e:
        # print(f"❌ Erro ao abrir ou salvar imagem: {e}")
        return None
