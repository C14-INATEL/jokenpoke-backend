from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)