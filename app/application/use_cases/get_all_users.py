from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.db.models.user_model import UserModel

class GetAllUsersUseCase:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def execute(self) -> list[UserModel]:
        # Busca todos os usuários já com suas cartas e decks atrelados
        users = self.user_repo.get_all_with_relations()
        return users