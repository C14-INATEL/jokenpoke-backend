from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.password import verify_password
from app.infrastructure.security.jwt_handler import create_token
from app.shared.exceptions.unauthorized_exception import UnauthorizedException


class LoginUserUseCase:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def execute(self, username: str, password: str) -> str:
        user = self.user_repo.get_by_username(username)

        if not user:
            raise UnauthorizedException("Credenciais inválidas")

        if not verify_password(password, user.password):
            raise UnauthorizedException("Credenciais inválidas")

        token = create_token(user.id)
        return token
