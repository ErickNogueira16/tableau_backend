# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app, origins=["https://tv-comercial-embed.vercel.app"])

TABLEAU_CLOUD_URL = os.environ["TABLEAU_CLOUD_URL"]  # Ex: https://us-east-1.online.tableau.com
API_VERSION = os.environ.get("API_VERSION", "3.21")
SITE_CONTENT_URL = os.environ["SITE_CONTENT_URL"]    # Ex: anabeatriz-8787706e44

PAT_NAME = os.environ["PAT_NAME"]
PAT_SECRET = os.environ["PAT_SECRET"]

WORKBOOK_NAME = "TVComercial-RaizzCapital_17543562925950"
DEFAULT_VIEW = "COMERCIALITAJA"

@app.route("/")
def home():
    return "✅ Backend da Raizz Capital - Tableau Token API"

@app.route("/get_tableau_url")
def get_tableau_url():
    """
    Cria sessão no Tableau Cloud via PAT e retorna URL de embed.
    """
    try:
        # 1️⃣ Autentica via PAT
        signin_url = f"{TABLEAU_CLOUD_URL}/api/{API_VERSION}/auth/signin"
        payload = {
            "credentials": {
                "personalAccessTokenName": PAT_NAME,
                "personalAccessTokenSecret": PAT_SECRET,
                "site": {"contentUrl": SITE_CONTENT_URL}
            }
        }
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        resp = requests.post(signin_url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        token = data["credentials"]["token"]
        site_id = data["credentials"]["site"]["id"]

        # 2️⃣ Retorna a URL de embed (não expõe token, só garante sessão)
        embed_url = f"{TABLEAU_CLOUD_URL}/t/{SITE_CONTENT_URL}/views/{WORKBOOK_NAME}/{DEFAULT_VIEW}?:embed=yes&:showAppBanner=false"

        return jsonify({"embed_url": embed_url, "site_id": site_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
