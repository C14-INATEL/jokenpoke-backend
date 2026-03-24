from app.domain.entities.pokemon import Pokemon

class Card:

    def __init__(
        self,
        pokemon: Pokemon,
        owner_id: int
    ):
        self.pokemon = pokemon
        self.owner_id = owner_id

    @property
    def name(self) -> str:
        return self.pokemon.name

    @property
    def element(self) -> str:
        return self.pokemon.move