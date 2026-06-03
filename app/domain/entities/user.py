from app.domain.entities.deck import Deck


class User:
    def __init__(
        self,
        id: int,
        username: str,
        deck: Deck | None = None,
        points: int = 0,
        rank: str = "Beginner",
    ):
        self.id = id
        self.username = username
        self.deck = deck
        self.points = points
        self.rank = rank

    def has_deck(self) -> bool:
        return self.deck is not None
