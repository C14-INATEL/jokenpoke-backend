from app.domain.entities.deck import Deck
from app.domain.entities.card import Card


class CreateDeckUseCase:

    def execute(self, selected_cards: list[Card]) -> Deck:

        if len(selected_cards) != 3:
            raise ValueError("O deck deve ter exatamente 3 cartas.")

        return Deck(cards=selected_cards)