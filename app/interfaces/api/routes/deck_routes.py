from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.application.use_cases.build_deck import BuildDeckUseCase
from app.schemas.deck_schema import BuildDeckRequest

router = APIRouter(prefix="/decks", tags=["Decks"])

@router.post("/{user_id}/build")
def build_deck(user_id: int, payload: BuildDeckRequest, db: Session = Depends(get_db)):
    use_case = BuildDeckUseCase(db)
    
    username = use_case.execute(user_id, payload.pokemon_ids)
    
    return {"message": f"Deck do usuário {username} montado com sucesso!"}