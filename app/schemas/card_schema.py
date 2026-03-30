from pydantic import BaseModel, ConfigDict

class CardResponse(BaseModel):
    id: int
    pokemon_id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)