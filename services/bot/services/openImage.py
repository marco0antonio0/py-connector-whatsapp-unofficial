from PIL import Image
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import automation


def openImage(self:"automation", image_path):
    try:
        # Abre a imagem
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao abrir a imagem: {e}")
        return None