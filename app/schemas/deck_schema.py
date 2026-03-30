from pydantic import BaseModel, ConfigDict

class DeckResponse(BaseModel):
    id: int
    user_id: int
    card_id: int

    model_config = ConfigDict(from_attributes=True)