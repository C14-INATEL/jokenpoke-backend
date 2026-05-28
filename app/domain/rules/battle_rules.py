from app.domain.rules.element_advantage import MOVE_WEAKNESS

ATTACKER_WINS = 1
DEFENDER_WINS = 2
DRAW = 0

WINNER_LABELS = {
    ATTACKER_WINS: "attacker",
    DEFENDER_WINS: "defender",
    DRAW: "draw",
}

def normalize_move(move: str) -> str:
    return move.strip().lower()


def resolve_move(attacker_move: str, defender_move: str) -> int:
    attacker_move = normalize_move(attacker_move)
    defender_move = normalize_move(defender_move)

    if attacker_move == defender_move:
        return DRAW

    if defender_move in MOVE_WEAKNESS.get(attacker_move, []):
        return DEFENDER_WINS

    if attacker_move in MOVE_WEAKNESS.get(defender_move, []):
        return ATTACKER_WINS

    return DRAW


def resolve_winner_label(result: int) -> str:
    return WINNER_LABELS.get(result, WINNER_LABELS[DRAW])
