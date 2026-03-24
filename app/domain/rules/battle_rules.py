MOVE_WEAKNESS = {
    "pedra": ["papel", "fogo", "corda"],
    "papel": ["tesoura", "agua", "fogo"],
    "tesoura": ["pedra", "agua", "fogo"],
    "corda": ["tesoura", "agua", "fogo", "papel"],
    "agua": ["pedra"],
    "fogo": ["agua"],
}


def resolve_move(move1: str, move2: str) -> int:
    """
    Retorna:
    1 -> jogador 1 vence
    2 -> jogador 2 vence
    0 -> empate
    """

    if move2 in MOVE_WEAKNESS.get(move1, []):
        return 2

    if move1 in MOVE_WEAKNESS.get(move2, []):
        return 1

    return 0