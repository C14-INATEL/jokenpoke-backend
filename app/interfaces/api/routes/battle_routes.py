from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.deck_repository import DeckRepository
from app.application.use_cases.start_battle import StartBattleUseCase

router = APIRouter(prefix="/battle", tags=["Battle"])


@router.post("/{defender_id}")
def battle(defender_id: int, db: Session = Depends(get_db)):
    attacker_id = 1  # depois JWT

    user_repo = UserRepository(db)
    deck_repo = DeckRepository(db)

    attacker = user_repo.get_by_id(attacker_id)
    defender = user_repo.get_by_id(defender_id)

    if not attacker or not defender:
        raise HTTPException(404)

    attacker.deck = deck_repo.get_user_deck(attacker.id)
    defender.deck = deck_repo.get_user_deck(defender.id)

    result = StartBattleUseCase().execute(attacker, defender)

    return result