import random
from typing import List

from app.domain.entities.card import Card


class Deck:
    def __init__(self, cards: List[Card]):
        if len(cards) != 3:
            raise ValueError("Um deck deve ter exatamente 3 cartas.")
        self.cards = cards

    def get_card(self, index: int) -> Card:
        return self.cards[index]

    def get_random_card(self) -> Card:
        return random.choice(self.cards)
