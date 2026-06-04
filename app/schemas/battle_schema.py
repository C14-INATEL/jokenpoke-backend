from pydantic import BaseModel

from app.schemas.pokemon_schema import PokemonResponse


class RoundResponse(BaseModel):
    round_number: int
    attacker_card: str
    defender_card: str
    attacker_move: str
    defender_move: str
    winner: str


class BattleRankingResponse(BaseModel):
    old_rank: str
    new_rank: str
    old_points: int
    new_points: int
    status: str
    message: str


class BattleResponse(BaseModel):
    rounds: list[RoundResponse]
    winner: str
    ranking: BattleRankingResponse | None = None
    reward_card: PokemonResponse | None = None
