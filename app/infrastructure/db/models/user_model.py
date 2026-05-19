from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relações virtuais para puxar os dados anexados
    cards = relationship(
        "CardModel", back_populates="owner", cascade="all, delete-orphan"
    )
    deck = relationship(
        "DeckModel", back_populates="user", cascade="all, delete-orphan"
    )
