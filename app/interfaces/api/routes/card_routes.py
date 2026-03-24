from fastapi import APIRouter

from app.infrastructure.repositories.pokemon_repository import PokemonRepository
from app.schemas.pokemon_schema import PokemonResponse

router = APIRouter(prefix="/pokemons", tags=["Pokemons"])

repository = PokemonRepository()


@router.get("/", response_model=list[PokemonResponse])
def get_all_pokemons():

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