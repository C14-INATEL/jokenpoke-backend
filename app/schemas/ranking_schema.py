from pydantic import BaseModel, ConfigDict


class RankingResponse(BaseModel):
    position: int
    username: str
    points: int
    rank: str

    model_config = ConfigDict(from_attributes=True)
