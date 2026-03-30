from sqlalchemy.orm import Session, selectinload
from app.infrastructure.db.models.user_model import UserModel
from app.domain.entities.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if not user:
            return None

        return User(id=user.id, username=user.username)

    def create(self, username: str, password: str) -> User:
        user = UserModel(username=username, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return User(id=user.id, username=user.username)
    
    def get_all_with_relations(self) -> list[UserModel]:
        users = (
            self.db.query(UserModel)
            .options(
                selectinload(UserModel.cards),
                selectinload(UserModel.deck)
            )
            .all()
        )
        return users