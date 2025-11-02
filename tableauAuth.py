import jwt
import datetime
import uuid

def generate_jwt(client_id, secret_key, secret_id, user_email, expires_minutes=10):
    now = datetime.datetime.utcnow()
    payload = {
        "iss": client_id,
        "sub": user_email,
        "aud": "tableau",
        "exp": now + datetime.timedelta(minutes=expires_minutes),
        "jti": str(uuid.uuid4()),
        "scp": ["tableau:views:embed"]
    }
    headers = {
        "kid": secret_id,
        "iss": client_id
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token