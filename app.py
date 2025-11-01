from flask import Flask, jsonify
from flask_cors import CORS
import os
import requests
from tableauAuth import tableau_pat_signin

app = Flask(__name__)
CORS(app, origins=["https://tv-comercial-embed.vercel.app"])

# Variáveis de ambiente obrigatórias
TABLEAU_CLOUD_URL = os.environ["TABLEAU_CLOUD_URL"]  
SITE_CONTENT_URL = os.environ["SITE_CONTENT_URL"]    
PAT_NAME = os.environ["PAT_NAME"]
PAT_SECRET = os.environ["PAT_SECRET"]

# Configuração do dashboard
WORKBOOK_NAME = "TVComercial-RaizzCapital_17543562925950"
DEFAULT_VIEW = "COMERCIALITAJA"

@app.route("/")
def home():
    return "✅ Backend da Raizz Capital - Tableau Token API (versão PAT)"

@app.route("/get_tableau_url")
def get_tableau_url():
    try:
        # 🔑 Autentica e obtém token + site_id
        token, site_id, user_id = tableau_pat_signin(
            tableau_base_url=TABLEAU_CLOUD_URL,
            site_content_url=SITE_CONTENT_URL,
            pat_name=PAT_NAME,
            pat_secret=PAT_SECRET
        )

        embed_url = (
            f"{TABLEAU_CLOUD_URL}/t/{SITE_CONTENT_URL}/views/"
            f"{WORKBOOK_NAME}/{DEFAULT_VIEW}?:embed=yes&:showAppBanner=false"
        )

        return jsonify({
            "embed_url": embed_url,
            "site_id": site_id,
            "user_id": user_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
