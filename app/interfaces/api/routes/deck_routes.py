from fastapi import APIRouter

from app.application.use_cases.build_deck import BuildDeckUseCase
from app.interfaces.api.dependencies import DbSession
from app.schemas.deck_schema import BuildDeckRequest

router = APIRouter(prefix="/decks", tags=["Decks"])


@router.post("/{user_id}/build")
def build_deck(user_id: int, payload: BuildDeckRequest, db: DbSession):
    use_case = BuildDeckUseCase(db)

    username = use_case.execute(user_id, payload.pokemon_ids)

    return {"message": f"Deck do usuário {username} montado com sucesso!"}
