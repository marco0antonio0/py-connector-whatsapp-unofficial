from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="py-connector-whatsapp-unofficial",
    version="0.0.1",
    license="MIT License",
    author="Marco Antonio",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="marcomesquitajr@hotmail.com",
    keywords=[
        "python whatsapp",
        "bot whatsapp unofficial",
        "connector whatsapp unofficial",
        "automation whatsapp unofficial",
    ],
    description="conector para envio e leitura de mensagem no whatsapp não oficial do whatsapp",
    packages=["bot"],
    install_requires=[
        "selenium",
        "webdriver-manager",
        "PyQRCode",
        "pillow",
    ],
)
