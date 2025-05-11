import subprocess
import os

MKDOCS_DIR = os.path.abspath(".")

def iniciar_mkdocs():
    print("🌐 Servindo documentação em http://localhost:3000 ...")
    subprocess.run(["mkdocs", "serve", "--dev-addr=0.0.0.0:3000"], cwd=MKDOCS_DIR)

if __name__ == "__main__":
    iniciar_mkdocs()
