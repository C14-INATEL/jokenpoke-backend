from dataclasses import dataclass


@dataclass
class RankingResult:
    username: str
    old_rank: str
    new_rank: str
    old_points: int
    new_points: int
    status: str  # "promoted" | "demoted" | "maintained"
    message: str
