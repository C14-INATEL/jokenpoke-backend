import random
from sqlalchemy.orm import Session
from app.domain.entities.card import Card
from app.infrastructure.repositories.pokemon_repository import PokemonRepository
from app.shared.exceptions.domain_exception import DomainException

class CardFactory:

    def __init__(self, db: Session):
        self.pokemon_repository = PokemonRepository(db)

    def create_random_cards(
        self,
        owner_id: int,
        quantity: int = 6
    ) -> list[Card]:

        pokemons = self.pokemon_repository.get_all()

        if len(pokemons) < quantity:
            raise DomainException(f"Not enough Pokemons in the database to generate {quantity} cards.")

        # evita repetição
        selected = random.sample(pokemons, k=quantity)

        return [
            Card(pokemon=p, owner_id=owner_id)
            for p in selected
        ]