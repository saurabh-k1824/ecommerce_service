import jwt
from datetime import datetime, timedelta
from django.conf import settings
import uuid


ACCESS_TOKEN_LIFETIME_MIN = 30
REFRESH_TOKEN_LIFETIME_DAYS = 1
JWT_ALGORITHM = "HS256"


def generate_access_token(payload: dict) -> str:
    data = payload.copy()
    data.update({
        "jti": str(uuid.uuid4()),
        "token_type": "access",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME_MIN),
    })

    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def generate_refresh_token(payload: dict) -> str:
    data = payload.copy()
    data.update({
        "jti": str(uuid.uuid4()),
        "token_type": "refresh",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS),
    })

    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={
                "require": ["exp"],
            },
        )
        return payload


    except Exception as e:
        raise (e)
