from sqlalchemy.orm import Session

from app.infrastructure.db.models.card_model import CardModel


class CardRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_many(self, cards):
        models = [
            CardModel(pokemon_id=card.pokemon.id, owner_id=card.owner_id)
            for card in cards
        ]

        self.db.add_all(models)
        self.db.commit()
