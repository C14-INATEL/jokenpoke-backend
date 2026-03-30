from pydantic import BaseModel, ConfigDict
from typing import List

from app.schemas.pokemon_schema import PokemonResponse
from app.schemas.deck_schema import DeckResponse

class UserResponse(BaseModel):
    id: int
    username: str
    
    cards: List[PokemonResponse] = []
    deck: List[DeckResponse] = []

    model_config = ConfigDict(from_attributes=True)