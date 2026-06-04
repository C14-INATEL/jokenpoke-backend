from sqlalchemy.orm import Session, selectinload

from app.domain.entities.user import User
from app.infrastructure.db.models.user_model import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if not user:
            return None

        return User(
            id=user.id, username=user.username, points=user.points, rank=user.rank
        )

    def create(self, username: str, password: str) -> User:
        user = UserModel(username=username, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return User(
            id=user.id, username=user.username, points=user.points, rank=user.rank
        )

    def get_all_with_relations(self) -> list[UserModel]:
        users = (
            self.db.query(UserModel)
            .options(selectinload(UserModel.cards), selectinload(UserModel.deck))
            .all()
        )
        return users

    def get_by_id_with_relations(self, user_id: int) -> UserModel | None:
        user = (
            self.db.query(UserModel)
            .filter(UserModel.id == user_id)
            .options(selectinload(UserModel.cards), selectinload(UserModel.deck))
            .first()
        )
        return user

    def get_by_username(self, username: str) -> UserModel | None:
        return self.db.query(UserModel).filter_by(username=username).first()

    def update(self, user_id: int, username: str) -> User:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user:
            user.username = username
            self.db.commit()
            self.db.refresh(user)
            return User(
                id=user.id, username=user.username, points=user.points, rank=user.rank
            )
        return None

    def delete(self, user_id: int) -> None:
        user = (
            self.db.query(UserModel)
            .filter(UserModel.id == user_id)
            .options(selectinload(UserModel.cards), selectinload(UserModel.deck))
            .first()
        )
        if user:
            self.db.delete(user)
            self.db.commit()

    def update_ranking(self, user_id: int, rank: str, points: int) -> UserModel | None:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if not user:
            return None
        user.rank = rank
        user.points = points
        self.db.commit()
        self.db.refresh(user)
        return user
