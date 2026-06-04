from dataclasses import dataclass

from app.domain.entities.pokemon import Pokemon


@dataclass
class RoundResult:
    round_number: int
    attacker_card: str
    defender_card: str
    attacker_move: str
    defender_move: str
    winner: str


@dataclass
class BattleResult:
    rounds: list[RoundResult]
    winner: str
    ranking: dict | None = None
    reward_card: Pokemon | None = None
