from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.infrastructure.security.jwt_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    return decode_token(token)
