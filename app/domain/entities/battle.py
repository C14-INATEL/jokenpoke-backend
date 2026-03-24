from dataclasses import dataclass
from typing import List


@dataclass
class RoundResult:
    round_number: int
    attacker_card: str
    defender_card: str
    winner: str  # "attacker" | "defender" | "draw"


@dataclass
class BattleResult:
    rounds: List[RoundResult]
    winner: str  # "attacker" | "defender" | "draw"