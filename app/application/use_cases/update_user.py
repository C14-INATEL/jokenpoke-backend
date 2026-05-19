from sqlalchemy.orm import Session

from app.infrastructure.repositories.user_repository import UserRepository
from app.shared.exceptions.not_found_exception import NotFoundException


class UpdateUserUseCase:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def execute(self, user_id: int, username: str) -> dict:
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise NotFoundException(f"Usuário com ID {user_id} não encontrado.")

        updated_user = self.user_repo.update(user_id, username)

        return {"id": updated_user.id, "username": updated_user.username}
