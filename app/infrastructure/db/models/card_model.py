from sqlalchemy import Column, Integer, ForeignKey
from app.infrastructure.db.base import Base


class CardModel(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))