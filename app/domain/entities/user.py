from __future__ import annotations
from typing import Optional
from app.domain.entities.deck import Deck


class User:

    def __init__(
        self,
        id: int,
        username: str,
        deck: Optional[Deck] = None
    ):
        self.id = id
        self.username = username
        self.deck = deck

    def assign_deck(self, deck: Deck) -> None:
        self.deck = deck

    def has_deck(self) -> bool:
        return self.deck is not None