from typing import List

from pydantic import BaseModel


class RoundResponse(BaseModel):
    round_number: int
    attacker_card: str
    defender_card: str
    winner: str


class BattleResponse(BaseModel):
    rounds: List[RoundResponse]
    winner: str
