from app.domain.rules.battle_rules import (
    ATTACKER_WINS,
    DEFENDER_WINS,
    DRAW,
    normalize_move,
    resolve_move,
    resolve_winner_label,
)


class TestNormalizeMove:
    def test_remove_espacos_inicio_e_fim(self):
        assert normalize_move("  pedra  ") == "pedra"

    def test_converte_para_minusculo(self):
        assert normalize_move("PEDRA") == "pedra"

    def test_remove_espacos_e_converte(self):
        assert normalize_move("  TESOURA  ") == "tesoura"

    def test_move_ja_normalizado(self):
        assert normalize_move("papel") == "papel"

    def test_move_vazio(self):
        assert normalize_move("  ") == ""


class TestResolveMove:
    # --- Empates ---
    def test_mesmo_move_retorna_draw(self):
        assert resolve_move("pedra", "pedra") == DRAW

    def test_moves_desconhecidos_retorna_draw(self):
        assert resolve_move("xyz", "abc") == DRAW

    def test_um_move_desconhecido_retorna_draw(self):
        assert resolve_move("pedra", "xyz") == DRAW

    def test_moves_normalizados_antes_de_comparar(self):
        assert resolve_move("  PEDRA  ", "pedra") == DRAW

    # --- Atacante vence ---
    def test_pedra_vence_tesoura(self):
        assert resolve_move("pedra", "tesoura") == ATTACKER_WINS

    def test_papel_vence_pedra(self):
        assert resolve_move("papel", "pedra") == ATTACKER_WINS

    def test_tesoura_vence_papel(self):
        assert resolve_move("tesoura", "papel") == ATTACKER_WINS

    def test_agua_vence_pedra(self):
        assert resolve_move("pedra", "agua") == ATTACKER_WINS

    def test_fogo_vence_papel(self):
        assert resolve_move("fogo", "papel") == ATTACKER_WINS

    def test_corda_vence_pedra(self):
        assert resolve_move("corda", "pedra") == ATTACKER_WINS

    # --- Defensor vence ---
    def test_tesoura_perde_para_pedra(self):
        assert resolve_move("tesoura", "pedra") == DEFENDER_WINS

    def test_pedra_perde_para_papel(self):
        assert resolve_move("pedra", "papel") == DEFENDER_WINS

    def test_papel_perde_para_tesoura(self):
        assert resolve_move("papel", "tesoura") == DEFENDER_WINS

    def test_pedra_perde_para_agua(self):
        assert resolve_move("agua", "pedra") == DEFENDER_WINS

    def test_papel_perde_para_fogo(self):
        assert resolve_move("papel", "fogo") == DEFENDER_WINS

    def test_pedra_perde_para_corda(self):
        assert resolve_move("pedra", "corda") == DEFENDER_WINS

    # --- Case-insensitive ---
    def test_case_insensitive_atacante(self):
        assert resolve_move("TESOURA", "pedra") == DEFENDER_WINS

    def test_case_insensitive_defensor(self):
        assert resolve_move("tesoura", "PEDRA") == DEFENDER_WINS

    def test_case_insensitive_ambos(self):
        assert resolve_move("PAPEL", "TESOURA") == DEFENDER_WINS


class TestResolveWinnerLabel:
    def test_retorna_attacker_para_ATTACKER_WINS(self):
        assert resolve_winner_label(ATTACKER_WINS) == "attacker"

    def test_retorna_defender_para_DEFENDER_WINS(self):
        assert resolve_winner_label(DEFENDER_WINS) == "defender"

    def test_retorna_draw_para_DRAW(self):
        assert resolve_winner_label(DRAW) == "draw"

    def test_retorna_draw_para_valor_desconhecido(self):
        assert resolve_winner_label(99) == "draw"

    def test_retorna_draw_para_valor_negativo(self):
        assert resolve_winner_label(-1) == "draw"
