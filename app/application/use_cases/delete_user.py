from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repository import UserRepository
from app.shared.exceptions.not_found_exception import NotFoundException

class DeleteUserUseCase:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def execute(self, user_id: int) -> str:
        user = self.user_repo.get_by_id(user_id)
        
        if not user:
            raise NotFoundException(f"Usuário com ID {user_id} não encontrado.")

        username = user.username 

        self.user_repo.delete(user_id)

        return username