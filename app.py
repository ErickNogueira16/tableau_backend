from flask import Flask, jsonify
from flask_cors import CORS
import os
from tableauAuth import generate_jwt_token

app = Flask(__name__)
CORS(app, origins=["https://tv-comercial-embed.vercel.app"])

# Variáveis de ambiente obrigatórias (Connected App)
TABLEAU_CLOUD_URL = os.environ["TABLEAU_CLOUD_URL"]  # Ex: https://us-east-1.online.tableau.com
SITE_CONTENT_URL = os.environ["SITE_CONTENT_URL"]     # Ex: anabeatriz-8787706e44
CLIENT_ID = os.environ["TABLEAU_CLIENT_ID"]
KEY_ID = os.environ["TABLEAU_KEY_ID"]
SECRET_VALUE = os.environ["TABLEAU_SECRET_VALUE"]
USER_EMAIL = os.environ["TABLEAU_USER_EMAIL"]

# Configuração do dashboard
WORKBOOK_NAME = "TVComercial-RaizzCapital_17543562925950"
DEFAULT_VIEW = "COMERCIALITAJA"

@app.route("/")
def home():
    return "✅ Backend da Raizz Capital - Tableau JWT API"

@app.route("/get_tableau_url")
def get_tableau_url():
    try:
        # 🔐 Gera JWT para autenticação segura
        jwt_token = generate_jwt_token(
            client_id=CLIENT_ID,
            key_id=KEY_ID,
            secret_key=SECRET_VALUE,
            user_email=USER_EMAIL
        )

        embed_url = (
            f"{TABLEAU_CLOUD_URL}/t/{SITE_CONTENT_URL}/views/"
            f"{WORKBOOK_NAME}/{DEFAULT_VIEW}"
            f"?:embed=yes&:showAppBanner=false&:jwt={jwt_token}"
        )

        return jsonify({"embed_url": embed_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)