from fastapi import APIRouter

from app.application.use_cases.start_battle import StartBattleUseCase
from app.application.use_cases.update_ranking import Ranking
from app.domain.factories.card_factory import CardFactory
from app.infrastructure.repositories.card_repository import CardRepository
from app.infrastructure.repositories.deck_repository import DeckRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.interfaces.api.dependencies import CurrentUser, DbSession
from app.schemas.battle_schema import BattleResponse
from app.shared.exceptions.not_found_exception import NotFoundException

router = APIRouter(prefix="/battle", tags=["Battle"])


@router.post(
    "/{defender_id}",
    response_model=BattleResponse,
    responses={
        404: {"description": "Atacante ou defensor não encontrado"},
    },
)
def battle(
    defender_id: int,
    attacker_id: CurrentUser,
    db: DbSession,
):
    user_repo = UserRepository(db)
    deck_repo = DeckRepository(db)

    attacker = user_repo.get_by_id(attacker_id)
    defender = user_repo.get_by_id(defender_id)

    if not attacker:
        raise NotFoundException(f"Atacante com ID {attacker_id} nao encontrado.")

    if not defender:
        raise NotFoundException(f"Defensor com ID {defender_id} nao encontrado.")

    attacker.deck = deck_repo.get_user_deck(attacker.id)
    defender.deck = deck_repo.get_user_deck(defender.id)

    result = StartBattleUseCase().execute(attacker, defender)

    if result.winner == "attacker":
        attacker_match_result = "vitoria"
    elif result.winner == "defender":
        attacker_match_result = "derrota"
    else:
        attacker_match_result = "empate"

    ranking_result = Ranking.calcular_novo_rank(
        rank_atual=attacker.rank,
        pontos_atuais=attacker.points,
        resultado_partida=attacker_match_result,
    )

    user_repo.update_ranking(
        user_id=attacker.id,
        rank=ranking_result["new_rank"],
        points=ranking_result["new_points"],
    )

    result.ranking = ranking_result

    if result.winner == "attacker":
        card_factory = CardFactory(db)
        card_repo = CardRepository(db)

        new_cards = card_factory.create_random_cards(
            owner_id=attacker.id,
            quantity=1,
        )
        card_repo.create_many(new_cards)

        result.reward_card = new_cards[0].pokemon

    return result
