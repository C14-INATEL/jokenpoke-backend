from fastapi import APIRouter

from app.infrastructure.repositories.pokemon_repository import PokemonRepository
from app.interfaces.api.dependencies import DbSession
from app.schemas.pokemon_schema import PokemonResponse

router = APIRouter(prefix="/pokemons", tags=["Pokemons"])


@router.get("/", response_model=list[PokemonResponse])
def get_all_pokemons(db: DbSession):
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
