import json
from pathlib import Path

from app.domain.entities.pokemon import Pokemon


class PokemonRepository:

    def __init__(self):
        self.file_path = Path("app/infrastructure/data/pokemons.json")

    def get_all(self) -> list[Pokemon]:
        with open(self.file_path, encoding="utf-8") as f:
            data = json.load(f)

        return [Pokemon(**p) for p in data]

    def get_by_id(self, pokemon_id: int) -> Pokemon | None:
        pokemons = self.get_all()
        for p in pokemons:
            if p.id == pokemon_id:
                return p
        return None