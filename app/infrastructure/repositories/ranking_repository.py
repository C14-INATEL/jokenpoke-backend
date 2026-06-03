from sqlalchemy.orm import Session

from app.infrastructure.db.models.user_model import UserModel


class RankingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_ranking_list(self) -> list[UserModel]:
        users = (
            self.db.query(UserModel)
            .order_by(UserModel.points.desc(), UserModel.id.asc())
            .all()
        )

        return users
