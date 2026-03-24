from sqlalchemy import Column, Integer, ForeignKey
from app.infrastructure.db.base import Base


class DeckModel(Base):
    __tablename__ = "deck"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))