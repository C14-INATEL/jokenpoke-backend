from app.domain.entities.deck import Deck


class User:
    def __init__(self, id: int, username: str, deck: Deck | None = None):
        self.id = id
        self.username = username
        self.deck = deck

    def has_deck(self) -> bool:
        return self.deck is not None
