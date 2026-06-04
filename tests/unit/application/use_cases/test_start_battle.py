from unittest.mock import MagicMock, patch

import pytest

from app.application.use_cases.start_battle import WINS_TO_FINISH, StartBattleUseCase
from app.domain.entities.battle import BattleResult, RoundResult
from app.shared.exceptions.domain_exception import DomainException
from tests.fixtures.battles import make_deck, make_user


@pytest.fixture
def use_case():
    return StartBattleUseCase()


class TestValidatePlayers:
    def test_mesmo_id_levanta_domain_exception(self, use_case):
        user = make_user(uid=1)
        with pytest.raises(DomainException, match="si mesmo"):
            use_case._validate_players(user, user)

    def test_atacante_sem_deck_levanta_domain_exception(self, use_case):
        attacker = make_user(uid=1, has_deck=False)
        defender = make_user(uid=2, has_deck=True)
        with pytest.raises(DomainException, match="atacante"):
            use_case._validate_players(attacker, defender)

    def test_defensor_sem_deck_levanta_domain_exception(self, use_case):
        attacker = make_user(uid=1, has_deck=True)
        defender = make_user(uid=2, has_deck=False)
        with pytest.raises(DomainException, match="defensor"):
            use_case._validate_players(attacker, defender)

    def test_jogadores_validos_nao_levanta_excecao(self, use_case, attacker, defender):
        use_case._validate_players(attacker, defender)


class TestResolveFinalWinner:
    def test_atacante_vence_quando_mais_wins(self, use_case):
        assert use_case._resolve_final_winner(2, 0) == "attacker"

    def test_defensor_vence_quando_mais_wins(self, use_case):
        assert use_case._resolve_final_winner(0, 2) == "defender"

    def test_empate_quando_wins_iguais(self, use_case):
        assert use_case._resolve_final_winner(1, 1) == "draw"

    def test_empate_quando_ambos_zero(self, use_case):
        assert use_case._resolve_final_winner(0, 0) == "draw"


class TestExecuteReturnStructure:
    def test_retorna_battle_result(self, use_case, attacker, defender):
        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        assert isinstance(result, BattleResult)

    def test_winner_eh_string_valida(self, use_case, attacker, defender):
        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        assert result.winner in ("attacker", "defender", "draw")

    def test_rounds_lista_de_round_result(self, use_case, attacker, defender):
        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        assert all(isinstance(r, RoundResult) for r in result.rounds)

    def test_round_result_tem_campos_corretos(self, use_case, attacker, defender):
        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        for i, r in enumerate(result.rounds, 1):
            assert r.round_number == i
            assert isinstance(r.attacker_card, str)
            assert isinstance(r.defender_card, str)
            assert r.winner in ("attacker", "defender", "draw")


class TestExecuteRoundCount:
    def test_para_quando_atacante_atinge_wins_to_finish(self, use_case):
        # atacante usa "papel" — vence "pedra" (defensor fixo)
        attacker = make_user(
            uid=1, has_deck=True, deck=make_deck(["papel", "papel", "papel"])
        )
        defender_deck = make_deck(["pedra", "pedra", "pedra"], owner_id=2)
        defender = make_user(uid=2, has_deck=True, deck=defender_deck)

        # Força defensor a sempre retornar a primeira carta (pedra)
        defender.deck.get_random_card = MagicMock(
            return_value=defender_deck.get_card(0)
        )

        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        assert len(result.rounds) == WINS_TO_FINISH
        assert result.winner == "attacker"

    def test_para_quando_defensor_atinge_wins_to_finish(self, use_case):
        # atacante usa "pedra" — perde para "papel" (defensor fixo)
        attacker = make_user(
            uid=1, has_deck=True, deck=make_deck(["pedra", "pedra", "pedra"])
        )
        defender_deck = make_deck(["papel", "papel", "papel"], owner_id=2)
        defender = make_user(uid=2, has_deck=True, deck=defender_deck)
        defender.deck.get_random_card = MagicMock(
            return_value=defender_deck.get_card(0)
        )

        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        assert len(result.rounds) == WINS_TO_FINISH
        assert result.winner == "defender"

    def test_respeita_limite_de_battle_rounds(self, use_case):
        attacker = make_user(
            uid=1, has_deck=True, deck=make_deck(["xyz", "xyz", "xyz"])
        )
        defender_deck = make_deck(["abc", "abc", "abc"], owner_id=2)
        defender = make_user(uid=2, has_deck=True, deck=defender_deck)
        defender.deck.get_random_card = MagicMock(
            return_value=defender_deck.get_card(0)
        )

        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 2
            result = use_case.execute(attacker, defender)

        assert len(result.rounds) <= 2

    def test_battle_rounds_maior_que_deck_usa_tamanho_do_deck(self, use_case):
        attacker = make_user(
            uid=1, has_deck=True, deck=make_deck(["xyz", "xyz", "xyz"])
        )
        defender_deck = make_deck(["abc", "abc", "abc"], owner_id=2)
        defender = make_user(uid=2, has_deck=True, deck=defender_deck)
        defender.deck.get_random_card = MagicMock(
            return_value=defender_deck.get_card(0)
        )

        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 999
            result = use_case.execute(attacker, defender)

        assert len(result.rounds) <= 3


class TestExecuteWinnerResolution:
    def test_empate_quando_todos_os_rounds_empatam(self, use_case):
        attacker = make_user(
            uid=1, has_deck=True, deck=make_deck(["pedra", "pedra", "pedra"])
        )
        defender_deck = make_deck(["pedra", "pedra", "pedra"], owner_id=2)
        defender = make_user(uid=2, has_deck=True, deck=defender_deck)
        defender.deck.get_random_card = MagicMock(
            return_value=defender_deck.get_card(0)
        )

        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        assert result.winner == "draw"

    def test_round_number_sequencial(self, use_case, attacker, defender):
        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        for i, r in enumerate(result.rounds, 1):
            assert r.round_number == i

    def test_nomes_das_cartas_nos_rounds(self, use_case):
        attacker_deck = make_deck(["pedra", "papel", "tesoura"], owner_id=1)
        attacker = make_user(uid=1, has_deck=True, deck=attacker_deck)

        defender_deck = make_deck(["pedra", "pedra", "pedra"], owner_id=2)
        defender = make_user(uid=2, has_deck=True, deck=defender_deck)
        defender.deck.get_random_card = MagicMock(
            return_value=defender_deck.get_card(0)
        )

        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 3
            result = use_case.execute(attacker, defender)

        card_names = {c.name for c in attacker_deck.cards}
        for r in result.rounds:
            assert r.attacker_card in card_names

    def test_moves_das_cartas_nos_rounds(self, use_case):
        attacker_deck = make_deck(["papel", "tesoura", "pedra"], owner_id=1)
        attacker = make_user(uid=1, has_deck=True, deck=attacker_deck)

        defender_deck = make_deck(["pedra", "pedra", "pedra"], owner_id=2)
        defender = make_user(uid=2, has_deck=True, deck=defender_deck)
        defender.deck.get_random_card = MagicMock(
            return_value=defender_deck.get_card(0)
        )

        with patch("app.application.use_cases.start_battle.settings") as mock_settings:
            mock_settings.battle_rounds = 1
            result = use_case.execute(attacker, defender)

        assert result.rounds[0].attacker_move == "papel"
        assert result.rounds[0].defender_move == "pedra"


class TestExecuteValidations:
    def test_mesmo_jogador_levanta_excecao(self, use_case):
        user = make_user(
            uid=1, has_deck=True, deck=make_deck(["pedra", "papel", "tesoura"])
        )
        with pytest.raises(DomainException):
            use_case.execute(user, user)

    def test_atacante_sem_deck_levanta_excecao(self, use_case, defender):
        attacker = make_user(uid=1, has_deck=False)
        with pytest.raises(DomainException):
            use_case.execute(attacker, defender)

    def test_defensor_sem_deck_levanta_excecao(self, use_case, attacker):
        defender = make_user(uid=2, has_deck=False)
        with pytest.raises(DomainException):
            use_case.execute(attacker, defender)
