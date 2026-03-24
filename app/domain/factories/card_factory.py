import random
from app.domain.entities.card import Card
from app.infrastructure.repositories.pokemon_repository import PokemonRepository


class CardFactory:

    def __init__(self):
        self.pokemon_repository = PokemonRepository()

    def create_random_cards(
        self,
        owner_id: int,
        quantity: int = 6
    ) -> list[Card]:

        pokemons = self.pokemon_repository.get_all()

        # evita repetição
        selected = random.sample(pokemons, k=quantity)

        return [
            Card(pokemon=p, owner_id=owner_id)
            for p in selected
        ]