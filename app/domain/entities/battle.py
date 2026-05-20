from dataclasses import dataclass


@dataclass
class RoundResult:
    round_number: int
    attacker_card: str
    defender_card: str
    winner: str  # "attacker" | "defender" | "draw"


@dataclass
class BattleResult:
    rounds: list[RoundResult]
    winner: str  # "attacker" | "defender" | "draw"
