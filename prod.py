import subprocess
import os
import http.server
import socketserver

MKDOCS_DIR = os.path.abspath(".")
SITE_DIR = os.path.join(MKDOCS_DIR, "site")
PORT = 3000

def build_mkdocs():
    print("⚙️ Gerando arquivos estáticos com MkDocs...")
    subprocess.run(["mkdocs", "build"], cwd=MKDOCS_DIR, check=True)

def servir_documentacao():
    os.chdir(SITE_DIR)
    print(f"🚀 Servindo documentação em http://localhost:{PORT}")
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    build_mkdocs()
    servir_documentacao()
