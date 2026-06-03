from pydantic import BaseModel, ConfigDict

from app.schemas.deck_schema import DeckResponse
from app.schemas.pokemon_schema import PokemonResponse


class UserResponse(BaseModel):
    id: int
    username: str
    points: int = 0
    rank: str

    cards: list[PokemonResponse] = []
    deck: list[DeckResponse] = []

    model_config = ConfigDict(from_attributes=True)
