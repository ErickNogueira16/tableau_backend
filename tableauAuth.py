import jwt
import uuid
import datetime

def generate_jwt_token(client_id, key_id, secret_key, user_email, expires_minutes=5):
    now = datetime.datetime.utcnow()

    payload = {
        "iss": client_id,
        "sub": user_email,
        "aud": "tableau",
        "exp": now + datetime.timedelta(minutes=expires_minutes),
        "jti": str(uuid.uuid4()),
        "scp": ["tableau:views:embed", "tableau:views:show"]
    }

    headers = {"kid": key_id}

    token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers)
    return token if isinstance(token, str) else token.decode("utf-8")