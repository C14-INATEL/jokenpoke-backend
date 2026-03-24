from sqlalchemy.orm import Session
from app.infrastructure.db.models.deck_model import DeckModel
from app.infrastructure.db.models.card_model import CardModel
from app.domain.entities.deck import Deck
from app.domain.entities.card import Card
from app.infrastructure.repositories.pokemon_repository import PokemonRepository


class DeckRepository:

    def __init__(self, db: Session):
        self.db = db
        self.pokemon_repo = PokemonRepository()

    def get_user_deck(self, user_id: int) -> Deck | None:
        deck_rows = self.db.query(DeckModel).filter_by(user_id=user_id).all()

        if not deck_rows:
            return None

        cards = []

        for row in deck_rows:
            card_row = self.db.query(CardModel).filter_by(id=row.card_id).first()
            pokemon = self.pokemon_repo.get_by_id(card_row.pokemon_id)

            cards.append(Card(pokemon=pokemon, owner_id=user_id))

        return Deck(cards)