from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings
from app.shared.exceptions.unauthorized_exception import UnauthorizedException


def create_token(user_id: int):
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(hours=2)}
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise UnauthorizedException("Token inválido.")

        return int(user_id)

    except (JWTError, ValueError):
        raise UnauthorizedException("Token inválido.") from None
