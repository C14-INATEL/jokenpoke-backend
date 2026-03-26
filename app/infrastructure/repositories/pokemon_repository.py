import json
from pathlib import Path
from sqlalchemy.orm import Session

from app.domain.entities.pokemon import Pokemon


class PokemonRepository:

    def __init__(self, db: Session):
        self.db = db
        self.file_path = Path("app/infrastructure/data/pokemons.json")
        self._cache = None

    def get_all(self) -> list[Pokemon]:

        if self._cache is None:
            with open(self.file_path, encoding="utf-8") as f:
                data = json.load(f)

            self._cache = [Pokemon(**p) for p in data]

        return self._cache

    def get_by_id(self, pokemon_id: int) -> Pokemon | None:
        return next(
            (p for p in self.get_all() if p.id == pokemon_id),
            None
        )