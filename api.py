from flask import Flask, request, jsonify
from threading import Thread
from services.bot.bot import automation
import time
from flasgger import Swagger
from flasgger.utils import swag_from

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
    bot_instance.start()
    print("🤖 Bot iniciado com sucesso!")

    while running:
        time.sleep(1)

@app.route('/start', methods=['POST'])
@swag_from('swagger.yml', endpoint='/start', methods=['POST'])
def start_bot():
    global bot_thread, running

    if bot_thread and bot_thread.is_alive():
        return jsonify({
            "status": "erro",
            "mensagem": "Bot já está em execução."
        }), 400

    bot_thread = Thread(target=bot_loop)
    bot_thread.start()
    return jsonify({
        "status": "sucesso",
        "mensagem": "Bot iniciado com sucesso."
    }), 200

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
                time.sleep(1)  # pequena pausa entre mensagens (ajustável)

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
