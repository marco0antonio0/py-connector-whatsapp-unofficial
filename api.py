from flask import Flask, request, jsonify, send_from_directory
from threading import Thread, Event
from queue import Queue
import threading
import time
import uuid
import qrcode
import os
from flasgger import Swagger
from flasgger.utils import swag_from
from services.bot.bot import automation

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yml')

# Estados globais
bot_instance = None
running = False

# Fila de tarefas
task_queue = Queue()

# Worker que processa uma tarefa por vez
def worker_loop():
    """
    Worker responsável por processar requisições da fila uma por vez.
    Utiliza app_context para manter o contexto da aplicação Flask ativo.
    """
    with app.app_context():
        while True:
            func, event, result_container = task_queue.get()
            try:
                result_container['response'] = func()
            except Exception as e:
                result_container['response'] = jsonify({"erro": str(e)}), 500
            finally:
                event.set()

# Inicia o worker
worker_thread = Thread(target=worker_loop, daemon=True)
worker_thread.start()

@app.route('/start', methods=['POST'])
@swag_from('swagger.yml', endpoint='/start', methods=['POST'])
def start_bot():
    """
    Inicia o bot WhatsApp.
    - Retorna erro se já estiver em execução.
    - Caso contrário, instancia e inicializa.
    """
    global bot_instance, running

    def task():
        global bot_instance, running
        if bot_instance:
            return jsonify({"status": "erro", "mensagem": "Bot já está em execução."}), 400
        bot_instance = automation(gui=False)
        running = True
        bot_instance.start_api()
        print("🤖 Bot iniciado com sucesso!")
        return jsonify({"status": "sucesso", "mensagem": "Bot iniciado com sucesso."}), 200

    event = Event()
    result = {}
    task_queue.put((task, event, result))
    event.wait()
    return result['response']

@app.route('/login', methods=['POST'])
@swag_from('swagger.yml', endpoint='/login', methods=['POST'])
def login_bot():
    """
    Realiza o processo de login no WhatsApp Web.
    - Se já estiver logado, retorna status.
    - Caso contrário, gera e retorna QRCode temporário.
    """
    global bot_instance

    host_url = request.host_url.rstrip("/")

    def task():
        if bot_instance:
            try:
                bot_instance.go_to_home()
                time.sleep(10)

                if bot_instance.checkIsLogin():
                    return jsonify({"status": "logado", "mensagem": "Bot já está logado no WhatsApp Web."}), 200

                qr_data = bot_instance.getDataRef()
                img_name = f"{uuid.uuid4().hex}.png"
                img_path = os.path.join("static", "qrcodes", img_name)

                qrcode.make(qr_data).save(img_path)

                threading.Timer(120, lambda: os.remove(img_path) if os.path.exists(img_path) else None).start()
                full_url = f"{host_url}/qrcode/{img_name}"

                return jsonify({
                    "status": "aguardando_login",
                    "mensagem": "Bot em execução aguardando leitura do QRCode.",
                    "qrCodeUrl": full_url
                }), 200
            except Exception as e:
                return jsonify({
                    "status": "erro",
                    "mensagem": "Erro ao verificar login.",
                    "erro": str(e)
                }), 500
        else:
            return jsonify({
                "status": "erro",
                "mensagem": "Bot ainda não foi iniciado. Use a rota /start."
            }), 400

    event = Event()
    result = {}
    task_queue.put((task, event, result))
    event.wait()
    return result['response']

@app.route('/qrcode/<filename>')
def serve_qrcode(filename):
    """
    Serve arquivos de imagem QRCode gerados no login.
    """
    return send_from_directory('static/qrcodes', filename)

@app.route('/status', methods=['GET'])
@swag_from('swagger.yml', endpoint='/status', methods=['GET'])
def bot_status():
    """
    Retorna o status atual do bot e se está logado no WhatsApp.
    """
    global bot_instance

    def task():
        if bot_instance is None:
            return jsonify({"status": "desligado", "logado": False, "mensagem": "Bot não está em execução."}), 200

        try:
            is_logged = bot_instance.checkIsLogin()
            return jsonify({"status": "ligado", "logado": bool(is_logged), "mensagem": "Status do bot obtido com sucesso."}), 200
        except Exception as e:
            return jsonify({"status": "ligado", "logado": False, "mensagem": "Erro ao verificar status do bot.", "erro": str(e)}), 500

    event = Event()
    result = {}
    task_queue.put((task, event, result))
    event.wait()
    return result['response']

@app.route('/send', methods=['POST'])
@swag_from('swagger.yml', endpoint='/send', methods=['POST'])
def send_message():
    """
    Envia uma lista de mensagens para um contato do WhatsApp.
    """
    global bot_instance

    data = request.get_json()
    contato = data.get("contato")
    mensagens = data.get("mensagens")

    if not contato or not mensagens or not isinstance(mensagens, list):
        return jsonify({
            "status": "erro",
            "mensagem": "Contato e mensagens são obrigatórios e devem estar no formato correto."
        }), 400

    def task():
        bot_instance.searchExistsContactAndOpen(contato)

        for mensagem in mensagens:
            if isinstance(mensagem, str) and mensagem.strip():
                bot_instance.enviar_mensagem_para_contato_aberto(mensagem)
                time.sleep(1)

        historico = bot_instance.pegar_todas_mensagens()
        bot_instance.go_to_home()

        return jsonify({
            "status": "sucesso",
            "mensagem": f"{len(mensagens)} mensagem(ns) enviada(s) para {contato}.",
            "dados": {
                "historico_mensagens": historico
            }
        }), 200

    event = Event()
    result = {}
    task_queue.put((task, event, result))
    event.wait()
    return result['response']

@app.route('/history/<contato>', methods=['GET'])
@swag_from('swagger.yml', endpoint='/history/{contato}', methods=['GET'])
def get_history(contato):
    """
    Obtém todas as mensagens trocadas com um contato específico.
    """
    global bot_instance

    def task():
        if bot_instance is None:
            return jsonify({"status": "erro", "mensagem": "Bot não está ativo."}), 400

        bot_instance.searchExistsContactAndOpen(contato)
        mensagens = bot_instance.pegar_todas_mensagens()
        bot_instance.go_to_home()

        return jsonify({
            "status": "sucesso",
            "mensagem": f"Mensagens recuperadas para {contato}.",
            "dados": {
                "mensagens": mensagens
            }
        }), 200

    event = Event()
    result = {}
    task_queue.put((task, event, result))
    event.wait()
    return result['response']

@app.route('/stop', methods=['POST'])
@swag_from('swagger.yml', endpoint='/stop', methods=['POST'])
def stop_bot():
    """
    Finaliza o bot e encerra a instância atual.
    """
    global running, bot_instance

    def task():
        global bot_instance, running
        running = False
        if bot_instance:
            bot_instance.exit()
            print("🛑 Bot encerrado.")
            bot_instance = None
        return jsonify({
            "status": "sucesso",
            "mensagem": "Bot finalizado com sucesso."
        }), 200

    event = Event()
    result = {}
    task_queue.put((task, event, result))
    event.wait()
    return result['response']

if __name__ == '__main__':
    app.run(debug=False, port=3000)
