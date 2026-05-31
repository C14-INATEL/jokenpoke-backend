from pydantic import BaseModel, ConfigDict


class RankingResponse(BaseModel):
    position: int
    username: str
    points: int

    model_config = ConfigDict(from_attributes=True)
