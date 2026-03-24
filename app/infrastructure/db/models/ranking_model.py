from sqlalchemy import Column, Integer, ForeignKey
from app.infrastructure.db.base import Base


class RankingModel(Base):
    __tablename__ = "ranking"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    points = Column(Integer, default=1000)