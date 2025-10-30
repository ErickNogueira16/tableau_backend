import jwt
import uuid
import datetime
import requests
import os

def generate_jwt(client_id, key_id, key_value, user_email, scopes=None, expires_minutes=5):
    now = datetime.datetime.utcnow()
    payload = {
        "iss": client_id,
        "sub": user_email,
        "aud": "tableau",
        "exp": now + datetime.timedelta(minutes=expires_minutes),
        "jti": str(uuid.uuid4())
    }
    if scopes:
        payload["scp"] = scopes
    headers = {"kid": key_id}
    token = jwt.encode(payload, key_value, algorithm="HS256", headers=headers)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def tableau_jwt_signin(tableau_base_url, api_version, jwt_token, site_content_url):
    url = f"{tableau_base_url}/api/{api_version}/auth/signin"
    body = {"credentials": {"jwt": jwt_token, "site": {"contentUrl": site_content_url}}}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    resp = requests.post(url, json=body, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    token = data["credentials"]["token"]
    site_id = data["credentials"]["site"]["id"]
    user_id = data["credentials"]["user"]["id"]
    return token, site_id, user_id
    