import os
import time
import traceback
import threading
import secrets
import argparse
from functools import wraps

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

from services.bot.bot import automation
from utils.bootstrap import bootstrap_main_config
from utils.cli import save_config
from utils.runtime_messages import print_system_started


def _parse_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "-r",
        "--reconfigure",
        action="store_true",
        help="Reabre o CLI para reconfigurar API key e webhook URL.",
    )
    args, _ = parser.parse_known_args()
    return args


ARGS = _parse_args()


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        provided = (request.headers.get("X-API-Key") or "").strip()
        auth_header = (request.headers.get("Authorization") or "").strip()

        if not provided and auth_header.lower().startswith("bearer "):
            provided = auth_header.split(" ", 1)[1].strip()

        expected = (runtime_state.get("api_key") or "").strip()
        if not expected or not provided or provided != expected:
            return jsonify({
                "status": "erro",
                "mensagem": "Unauthorized: API key inválida ou ausente.",
            }), 401
        return func(*args, **kwargs)

    return wrapper


config = bootstrap_main_config(force_reconfigure=ARGS.reconfigure)
instance = automation(gui=config.get("gui", False))
instance.start()
print_system_started()

app = Flask(__name__)
CORS(app)
swagger = Swagger(app, template_file="swagger_main.yml")

selenium_lock = threading.RLock()
runtime_state = {
    "webhook_url": (config.get("webhook_url") or "").strip(),
    "api_key": (config.get("api_key") or "").strip(),
}

def _persist_runtime_preferences():
    config["webhook_url"] = (runtime_state.get("webhook_url") or "").strip()
    config["api_key"] = (runtime_state.get("api_key") or "").strip()
    save_config(config)


if not runtime_state["api_key"]:
    runtime_state["api_key"] = secrets.token_urlsafe(24)
    _persist_runtime_preferences()
    print("🔐 api_key gerada automaticamente e salva em config.json")
    print(f"🔐 api_key: {runtime_state['api_key']}")


def _open_contact_and_get_history(contato: str):
    encontrou = instance.abrir_conversa_por_identificador(contato)
    if not encontrou:
        return False, []
    history = instance.pegar_todas_mensagens()
    return True, history


def _post_webhook(payload: dict):
    webhook_url = runtime_state.get("webhook_url", "").strip()
    print(f"🔗 Enviando payload para webhook: {webhook_url}")
    if not webhook_url:
        return

    try:
        response = requests.post(webhook_url, json=payload, timeout=50)
        if response.status_code >= 300:
            print(f"⚠️ Webhook respondeu status {response.status_code}")
    except Exception as e:
        print(f"❌ Falha ao enviar webhook: {e}")


@instance.run(block=False)
@instance.hook_new_message()
def on_new_message(payload=None):
    contato = instance.hook_new_message.contato
    print(f"📨 Nova mensagem de: {contato}")

    history = []
    identifier_info = {}
    try:
        with selenium_lock:
            encontrou, history = _open_contact_and_get_history(contato)
            if not encontrou:
                print(f"⚠️ Não foi possível abrir a conversa de '{contato}'.")
                return
            identifier_info = instance.identificar_contato(contato)
    except Exception as e:
        print(f"❌ Erro ao processar nova mensagem: {e}")
        traceback.print_exc()
    finally:
        with selenium_lock:
            instance.go_to_home()

    webhook_payload = {
        "event": "new_message",
        "contact": contato,
        "timestamp": int(time.time()),
        "history": history,
        "last_message": history[-1] if history else None,
        "identifier": identifier_info,
        "source_payload": payload or {},
    }
    _post_webhook(webhook_payload)


@app.get("/health")
@swag_from("swagger_main.yml", endpoint="/health", methods=["GET"])
@require_api_key
def health():
    return jsonify({"status": "ok", "running": True}), 200


@app.post("/api/webhook")
@swag_from("swagger_main.yml", endpoint="/api/webhook", methods=["POST"])
@require_api_key
def set_webhook():
    data = request.get_json(silent=True) or {}
    webhook_url = (data.get("webhook_url") or "").strip()
    old_value = runtime_state.get("webhook_url", "")

    runtime_state["webhook_url"] = webhook_url
    _persist_runtime_preferences()

    persisted_value = (config.get("webhook_url") or "").strip()
    return jsonify({
        "status": "ok",
        "webhook_url": webhook_url,
        "previous_webhook_url": old_value,
        "persisted": persisted_value == webhook_url,
    }), 200


@app.post("/api/send")
@swag_from("swagger_main.yml", endpoint="/api/send", methods=["POST"])
@require_api_key
def api_send_message():
    data = request.get_json(silent=True) or {}
    contato = (data.get("contato") or "").strip()
    mensagem = (data.get("mensagem") or "").strip()
    mensagens = data.get("mensagens")

    if not contato:
        return jsonify({"status": "erro", "mensagem": "Campo 'contato' é obrigatório."}), 400

    if isinstance(mensagens, list):
        queue = [str(m).strip() for m in mensagens if str(m).strip()]
    else:
        queue = [mensagem] if mensagem else []

    if not queue:
        return jsonify({"status": "erro", "mensagem": "Informe 'mensagem' ou 'mensagens'."}), 400

    try:
        with selenium_lock:
            identifier_info = instance.identificar_contato(contato)
            encontrou, _ = _open_contact_and_get_history(contato)
            if not encontrou:
                return jsonify({
                    "status": "erro",
                    "mensagem": f"Contato '{contato}' não encontrado/aberto.",
                    "identifier": identifier_info,
                }), 404

            enviados = 0
            for item in queue:
                if instance.enviar_mensagem_para_contato_aberto(item):
                    enviados += 1
            history = instance.pegar_todas_mensagens()
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    finally:
        with selenium_lock:
            instance.go_to_home()

    return jsonify({
        "status": "sucesso",
        "contato": contato,
        "identifier": identifier_info,
        "enviados": enviados,
        "history": history,
    }), 200


@app.get("/api/history/<path:contato>")
@swag_from("swagger_main.yml", endpoint="/api/history/{contato}", methods=["GET"])
@require_api_key
def api_history(contato: str):
    contato = contato.strip()
    if not contato:
        return jsonify({"status": "erro", "mensagem": "Contato inválido."}), 400

    try:
        with selenium_lock:
            identifier_info = instance.identificar_contato(contato)
            encontrou, history = _open_contact_and_get_history(contato)
            if not encontrou:
                return jsonify({"status": "erro", "mensagem": f"Contato '{contato}' não encontrado."}), 404
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    finally:
        with selenium_lock:
            instance.go_to_home()

    return jsonify({
        "status": "sucesso",
        "contato": contato,
        "identifier": identifier_info,
        "history": history,
    }), 200


@app.post("/api/history")
@swag_from("swagger_main.yml", endpoint="/api/history", methods=["POST"])
@require_api_key
def api_history_post():
    data = request.get_json(silent=True) or {}
    contato = (data.get("contato") or "").strip()
    if not contato:
        return jsonify({"status": "erro", "mensagem": "Campo 'contato' é obrigatório."}), 400
    return api_history(contato)


if __name__ == "__main__":
    port = int(config.get("api_port", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)
