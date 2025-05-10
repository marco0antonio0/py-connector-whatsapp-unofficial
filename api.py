from flask import Flask, request, jsonify,send_from_directory
from threading import Thread
import threading
from services.bot.bot import automation
import time
from flasgger import Swagger
from flasgger.utils import swag_from
import qrcode
import uuid
import os

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yml')


bot_thread = None
bot_instance = None
running = False

def bot_loop():
    global running, bot_instance
    if bot_instance is None:
        bot_instance = automation(gui=False)
    else:
        print("⚠️ Bot já iniciado.")
        return

    running = True
    bot_instance.start_api()
    print("🤖 Bot iniciado com sucesso!")

    while running:
        time.sleep(1)


@app.route('/login', methods=['POST'])
def login_bot():
    global bot_thread, bot_instance, running

    # print("🔄 Rota /login acionada")

    if bot_instance:
        # print("✅ bot_instance existe")
        try:
            # print("➡️ Acessando a tela inicial do WhatsApp Web...")
            bot_instance.go_to_home()
            time.sleep(10)
            # print("⏳ Verificando se já está logado...")

            if bot_instance.checkIsLogin():
                # print("✅ Bot já está logado")
                return jsonify({
                    "status": "logado",
                    "mensagem": "Bot já está logado no WhatsApp Web."
                }), 200
            else:
                # print("⚠️ Bot não está logado, gerando QRCode...")
                qr_data = bot_instance.getDataRef()
                img_name = f"{uuid.uuid4().hex}.png"
                img_path = os.path.join("static", "qrcodes", img_name)

                # print(f"📦 Salvando QRCode em: {img_path}")
                qr_img = qrcode.make(qr_data)
                qr_img.save(img_path)

                # print("⏲️ Iniciando temporizador para remover QRCode em 2 minutos")
                threading.Timer(120, lambda: os.remove(img_path) if os.path.exists(img_path) else None).start()

                full_url = request.host_url.rstrip("/") + f"/qrcode/{img_name}"
                # print(f"📤 QRCode disponível em: {full_url}")

                return jsonify({
                    "status": "aguardando_login",
                    "mensagem": "Bot em execução aguardando leitura do QRCode.",
                    "qrCodeUrl": full_url
                }), 200

        except Exception as e:
            # print(f"❌ Erro ao verificar login: {e}")
            return jsonify({
                "status": "erro",
                "mensagem": "Erro ao verificar login.",
                "erro": str(e)
            }), 500

    else:
        # print("❌ bot_instance está None — o bot não foi iniciado")
        return jsonify({
            "status": "erro",
            "mensagem": "Bot ainda não foi iniciado. Use a rota /start ou inicialize o bot."
        }), 400


@app.route('/start', methods=['POST'])
@swag_from('swagger.yml', endpoint='/start', methods=['POST'])
def start_bot():
    global bot_instance, running

    if bot_instance:
        return jsonify({
            "status": "erro",
            "mensagem": "Bot já está em execução."
        }), 400

    try:
        bot_instance = automation(gui=False)
        running = True
        bot_instance.start_api()
        print("🤖 Bot iniciado com sucesso!")

        return jsonify({
            "status": "sucesso",
            "mensagem": "Bot iniciado com sucesso."
        }), 200
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao iniciar o bot.",
            "erro": str(e)
        }), 500

@app.route('/qrcode/<filename>')
def serve_qrcode(filename):
    return send_from_directory('static/qrcodes', filename)

@app.route('/status', methods=['GET'])
@swag_from('swagger.yml', endpoint='/status', methods=['GET'])
def bot_status():
    if bot_instance is None:
        return jsonify({
            "status": "desligado",
            "logado": False,
            "mensagem": "Bot não está em execução."
        }), 200

    try:
        is_logged = bot_instance.checkIsLogin()
        return jsonify({
            "status": "ligado",
            "logado": bool(is_logged),
            "mensagem": "Status do bot obtido com sucesso."
        }), 200
    except Exception as e:
        return jsonify({
            "status": "ligado",
            "logado": False,
            "mensagem": "Erro ao verificar status do bot.",
            "erro": str(e)
        }), 500

@app.route('/send', methods=['POST'])
@swag_from('swagger.yml', endpoint='/send', methods=['POST'])
def send_message():
    if bot_instance is None:
        return jsonify({
            "status": "erro",
            "mensagem": "Bot não está ativo."
        }), 400

    data = request.get_json()
    contato = data.get("contato")
    mensagens = data.get("mensagens")

    if not contato or not mensagens:
        return jsonify({
            "status": "erro",
            "mensagem": "Contato e mensagens são obrigatórios."
        }), 400

    if not isinstance(mensagens, list):
        return jsonify({
            "status": "erro",
            "mensagem": "O campo 'mensagens' deve ser uma lista de strings."
        }), 400

    try:
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
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao enviar mensagens.",
            "erro": str(e)
        }), 500

@app.route('/history/<contato>', methods=['GET'])
@swag_from('swagger.yml', endpoint='/history/{contato}', methods=['GET'])
def get_history(contato):
    if bot_instance is None:
        return jsonify({
            "status": "erro",
            "mensagem": "Bot não está ativo."
        }), 400

    try:
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
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro ao buscar histórico.",
            "erro": str(e)
        }), 500

@app.route('/stop', methods=['POST'])
@swag_from('swagger.yml', endpoint='/stop', methods=['POST'])
def stop_bot():
    global running, bot_instance
    running = False
    if bot_instance:
        bot_instance.exit()
        print("🛑 Bot encerrado.")
        bot_instance = None
    return jsonify({
        "status": "sucesso",
        "mensagem": "Bot finalizado com sucesso."
    }), 200

if __name__ == '__main__':
    app.run(debug=False,port=3000)
