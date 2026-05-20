from pydantic import BaseModel, ConfigDict, Field


class DeckResponse(BaseModel):
    id: int
    user_id: int
    card_id: int

    model_config = ConfigDict(from_attributes=True)


class BuildDeckRequest(BaseModel):
    pokemon_ids: list[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Lista com exatamente 3 IDs de Pokémons",
    )
