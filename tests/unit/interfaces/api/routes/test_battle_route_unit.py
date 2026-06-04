import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.domain.entities.battle import BattleResult

sys.modules["app.core.config"].settings.database_url = "sqlite:///:memory:"


def _battle_route():
    from app.interfaces.api.routes.battle_routes import battle

    return battle


def _make_user(user_id: int, rank: str = "Beginner", points: int = 0):
    return SimpleNamespace(id=user_id, rank=rank, points=points, deck=None)


def _make_reward_card():
    pokemon = SimpleNamespace(
        id=25,
        name="Pikachu",
        move="thunder",
        description="Electric mouse",
    )
    return SimpleNamespace(pokemon=pokemon)


@patch("app.interfaces.api.routes.battle_routes.CardRepository")
@patch("app.interfaces.api.routes.battle_routes.CardFactory")
@patch("app.interfaces.api.routes.battle_routes.Ranking")
@patch("app.interfaces.api.routes.battle_routes.StartBattleUseCase")
@patch("app.interfaces.api.routes.battle_routes.DeckRepository")
@patch("app.interfaces.api.routes.battle_routes.UserRepository")
def test_battle_updates_ranking_and_rewards_attacker_win(
    user_repo_cls,
    deck_repo_cls,
    start_battle_cls,
    ranking_cls,
    card_factory_cls,
    card_repo_cls,
):
    db_mock = MagicMock()
    attacker = _make_user(user_id=1, rank="Beginner", points=80)
    defender = _make_user(user_id=2)
    user_repo = user_repo_cls.return_value
    user_repo.get_by_id.side_effect = [attacker, defender]
    deck_repo_cls.return_value.get_user_deck.side_effect = [
        "attacker-deck",
        "defender-deck",
    ]
    battle_result = BattleResult(rounds=[], winner="attacker")
    start_battle_cls.return_value.execute.return_value = battle_result
    ranking_result = {
        "old_rank": "Beginner",
        "new_rank": "Great",
        "old_points": 80,
        "new_points": 5,
        "status": "rank_up",
        "message": "rank up",
    }
    ranking_cls.calcular_novo_rank.return_value = ranking_result
    reward_card = _make_reward_card()
    card_factory_cls.return_value.create_random_cards.return_value = [reward_card]

    result = _battle_route()(defender_id=2, attacker_id=1, db=db_mock)

    assert result is battle_result
    assert result.ranking == ranking_result
    assert result.reward_card is reward_card.pokemon
    ranking_cls.calcular_novo_rank.assert_called_once_with(
        rank_atual="Beginner",
        pontos_atuais=80,
        resultado_partida="vitoria",
    )
    user_repo.update_ranking.assert_called_once_with(
        user_id=1,
        rank="Great",
        points=5,
    )
    card_factory_cls.return_value.create_random_cards.assert_called_once_with(
        owner_id=1,
        quantity=1,
    )
    card_repo_cls.return_value.create_many.assert_called_once_with([reward_card])


@patch("app.interfaces.api.routes.battle_routes.CardRepository")
@patch("app.interfaces.api.routes.battle_routes.CardFactory")
@patch("app.interfaces.api.routes.battle_routes.Ranking")
@patch("app.interfaces.api.routes.battle_routes.StartBattleUseCase")
@patch("app.interfaces.api.routes.battle_routes.DeckRepository")
@patch("app.interfaces.api.routes.battle_routes.UserRepository")
def test_battle_updates_ranking_without_reward_when_attacker_loses(
    user_repo_cls,
    deck_repo_cls,
    start_battle_cls,
    ranking_cls,
    card_factory_cls,
    card_repo_cls,
):
    db_mock = MagicMock()
    attacker = _make_user(user_id=1, rank="Great", points=10)
    defender = _make_user(user_id=2)
    user_repo = user_repo_cls.return_value
    user_repo.get_by_id.side_effect = [attacker, defender]
    deck_repo_cls.return_value.get_user_deck.side_effect = [
        "attacker-deck",
        "defender-deck",
    ]
    battle_result = BattleResult(rounds=[], winner="defender")
    start_battle_cls.return_value.execute.return_value = battle_result
    ranking_result = {
        "old_rank": "Great",
        "new_rank": "Beginner",
        "old_points": 10,
        "new_points": 75,
        "status": "rank_down",
        "message": "rank down",
    }
    ranking_cls.calcular_novo_rank.return_value = ranking_result

    result = _battle_route()(defender_id=2, attacker_id=1, db=db_mock)

    assert result is battle_result
    assert result.ranking == ranking_result
    assert result.reward_card is None
    ranking_cls.calcular_novo_rank.assert_called_once_with(
        rank_atual="Great",
        pontos_atuais=10,
        resultado_partida="derrota",
    )
    user_repo.update_ranking.assert_called_once_with(
        user_id=1,
        rank="Beginner",
        points=75,
    )
    card_factory_cls.assert_not_called()
    card_repo_cls.assert_not_called()


@patch("app.interfaces.api.routes.battle_routes.CardRepository")
@patch("app.interfaces.api.routes.battle_routes.CardFactory")
@patch("app.interfaces.api.routes.battle_routes.Ranking")
@patch("app.interfaces.api.routes.battle_routes.StartBattleUseCase")
@patch("app.interfaces.api.routes.battle_routes.DeckRepository")
@patch("app.interfaces.api.routes.battle_routes.UserRepository")
def test_battle_updates_ranking_without_reward_when_draw(
    user_repo_cls,
    deck_repo_cls,
    start_battle_cls,
    ranking_cls,
    card_factory_cls,
    card_repo_cls,
):
    db_mock = MagicMock()
    attacker = _make_user(user_id=1, rank="Beginner", points=50)
    defender = _make_user(user_id=2)
    user_repo = user_repo_cls.return_value
    user_repo.get_by_id.side_effect = [attacker, defender]
    deck_repo_cls.return_value.get_user_deck.side_effect = [
        "attacker-deck",
        "defender-deck",
    ]
    battle_result = BattleResult(rounds=[], winner="draw")
    start_battle_cls.return_value.execute.return_value = battle_result
    ranking_result = {
        "old_rank": "Beginner",
        "new_rank": "Beginner",
        "old_points": 50,
        "new_points": 50,
        "status": "maintained",
        "message": "draw",
    }
    ranking_cls.calcular_novo_rank.return_value = ranking_result

    result = _battle_route()(defender_id=2, attacker_id=1, db=db_mock)

    assert result is battle_result
    assert result.ranking == ranking_result
    assert result.reward_card is None
    ranking_cls.calcular_novo_rank.assert_called_once_with(
        rank_atual="Beginner",
        pontos_atuais=50,
        resultado_partida="empate",
    )
    user_repo.update_ranking.assert_called_once_with(
        user_id=1,
        rank="Beginner",
        points=50,
    )
    card_factory_cls.assert_not_called()
    card_repo_cls.assert_not_called()
