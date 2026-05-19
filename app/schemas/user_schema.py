from typing import List

from pydantic import BaseModel, ConfigDict

from app.schemas.deck_schema import DeckResponse
from app.schemas.pokemon_schema import PokemonResponse


class UserResponse(BaseModel):
    id: int
    username: str

    cards: List[PokemonResponse] = []
    deck: List[DeckResponse] = []

    model_config = ConfigDict(from_attributes=True)
