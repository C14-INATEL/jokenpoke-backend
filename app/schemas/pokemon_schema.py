from pydantic import BaseModel

class PokemonResponse(BaseModel):
    id: int
    name: str
    move: str
    description: str