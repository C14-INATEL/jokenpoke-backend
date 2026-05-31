from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.use_cases.start_battle import StartBattleUseCase
from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.deck_repository import DeckRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.auth_dependencies import get_current_user_id
from app.schemas.battle_schema import BattleResponse
from app.shared.exceptions.not_found_exception import NotFoundException

router = APIRouter(prefix="/battle", tags=["Battle"])


@router.post("/{defender_id}", response_model=BattleResponse)
def battle(
    defender_id: int,
    attacker_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
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

    return result
