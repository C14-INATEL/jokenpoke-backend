# tests/unit/infrastructure/test_pokemon_repository.py
import json

from app.infrastructure.repositories.pokemon_repository import PokemonRepository


class TestPokemonRepository:
    def test_pokemon_repository_leitura_json(self, tmp_path):
        data = [
            {
                "id": 1,
                "original_name": "Bulbasaur",
                "name": "Bulbasaur",
                "move": "vine whip",
                "description": "A strange seed was planted on its back at birth.",
            },
            {
                "id": 4,
                "original_name": "Charmander",
                "name": "Charmander",
                "move": "ember",
                "description": "Obviously prefers hot places.",
            },
        ]

        file_path = tmp_path / "pokemons.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        repo = PokemonRepository(db=None)
        repo.file_path = file_path

        pokemons = repo.get_all()

        assert len(pokemons) == 2
        assert pokemons[0].name == "Bulbasaur"
        assert pokemons[1].id == 4

    def test_pokemon_repository_cache(self, tmp_path):
        data = [
            {
                "id": 25,
                "original_name": "Pikachu",
                "name": "Pikachu",
                "move": "thunderbolt",
                "description": "Electric mouse.",
            }
        ]

        file_path = tmp_path / "pokemons.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        repo = PokemonRepository(db=None)
        repo.file_path = file_path

        first_call = repo.get_all()
        second_call = repo.get_all()

        assert repo._cache is not None
        assert first_call is second_call

    def test_get_by_id_should_return_pokemon(self, tmp_path):
        data = [
            {
                "id": 150,
                "original_name": "Mewtwo",
                "name": "Mewtwo",
                "move": "psychic",
                "description": "Genetic Pokémon.",
            }
        ]

        file_path = tmp_path / "pokemons.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        repo = PokemonRepository(db=None)
        repo.file_path = file_path

        pokemon = repo.get_by_id(150)

        assert pokemon is not None
        assert pokemon.name == "Mewtwo"

    def test_get_by_id_should_return_none_when_not_found(self, tmp_path):
        data = []

        file_path = tmp_path / "pokemons.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        repo = PokemonRepository(db=None)
        repo.file_path = file_path

        pokemon = repo.get_by_id(999)

        assert pokemon is None

    def test_cache_should_not_reload_file_after_first_read(self, tmp_path):
        data = [
            {
                "id": 1,
                "original_name": "Bulbasaur",
                "name": "Bulbasaur",
                "move": "vine whip",
                "description": "Grass Pokémon",
            }
        ]

        file_path = tmp_path / "pokemons.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        repo = PokemonRepository(db=None)
        repo.file_path = file_path

        first_call = repo.get_all()

        file_path.write_text("[]", encoding="utf-8")

        second_call = repo.get_all()

        assert len(second_call) == 1
        assert first_call is second_call
