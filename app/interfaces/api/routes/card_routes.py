from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.pokemon_repository import PokemonRepository
from app.schemas.pokemon_schema import PokemonResponse

router = APIRouter(prefix="/pokemons", tags=["Pokemons"])


@router.get("/", response_model=list[PokemonResponse])
def get_all_pokemons(
    db: Session = Depends(get_db),
):  # <-- 1. Injete a sessão do banco aqui

    # 2. Instancie o repositório DENTRO da rota, repassando o db
    repository = PokemonRepository(db)

    pokemons = repository.get_all()

    return [
        PokemonResponse(
            id=p.id,
            name=p.name,
            move=p.move,
            description=p.description,
        )
        for p in pokemons
    ]
