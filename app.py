from flask import Flask, jsonify
from flask_cors import CORS
import os
from tableauAuth import generate_jwt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 Lendo variáveis de ambiente
CONNECTED_APP_CLIENT_ID = os.environ["CONNECTED_APP_CLIENT_ID"]
CONNECTED_APP_KEY_ID = os.environ["CONNECTED_APP_KEY_ID"]
CONNECTED_APP_KEY_VALUE = os.environ["CONNECTED_APP_KEY_VALUE"]
TABLEAU_USER_EMAIL = os.environ["TABLEAU_USER_EMAIL"]

TABLEAU_CLOUD_URL = os.environ["TABLEAU_CLOUD_URL"]
SITE_CONTENT_URL = os.environ["SITE_CONTENT_URL"]

WORKBOOK_NAME = "TVComercial-RaizzCapital_17543562925950"
DEFAULT_VIEW = "COMERCIALITAJA"

@app.route("/")
def home():
    return "✅ Backend da Raizz Capital - Tableau Token API (JWT)"

@app.route("/get_tableau_url")
def get_tableau_url():
    try:
        # 🔑 Gera JWT
        token = generate_jwt(
            client_id=CONNECTED_APP_CLIENT_ID,
            secret_key=CONNECTED_APP_KEY_VALUE,
            secret_id=CONNECTED_APP_KEY_ID,
            user_email=TABLEAU_USER_EMAIL
        )

        embed_url = (
            f"{TABLEAU_CLOUD_URL}/t/{SITE_CONTENT_URL}/views/"
            f"{WORKBOOK_NAME}/{DEFAULT_VIEW}?:embed=yes&:showAppBanner=false"
        )

        return jsonify({
            "embed_url": embed_url,
            "jwt": token
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
