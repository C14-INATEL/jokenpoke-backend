from pydantic import BaseModel, ConfigDict
from typing import List

from app.schemas.card_schema import CardResponse
from app.schemas.deck_schema import DeckResponse

class UserResponse(BaseModel):
    id: int
    username: str
    
    cards: List[CardResponse] = []
    deck: List[DeckResponse] = []

    model_config = ConfigDict(from_attributes=True)