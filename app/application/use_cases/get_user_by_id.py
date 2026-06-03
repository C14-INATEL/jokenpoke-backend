from sqlalchemy.orm import Session

from app.infrastructure.repositories.pokemon_repository import PokemonRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.shared.exceptions.not_found_exception import NotFoundException


class GetUserByIdUseCase:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.pokemon_repo = PokemonRepository(db)

    def execute(self, user_id: int) -> dict:
        user = self.user_repo.get_by_id_with_relations(user_id)

        if not user:
            raise NotFoundException(f"Usuário com ID {user_id} não encontrado.")

        enriched_collection = []
        enriched_deck = []

        for card in user.cards:
            poke = self.pokemon_repo.get_by_id(card.pokemon_id)
            if poke:
                enriched_collection.append(
                    {
                        "id": poke.id,
                        "name": poke.name,
                        "move": poke.move,
                        "description": poke.description,
                    }
                )

        for deck_item in user.deck:
            card_obj = next((c for c in user.cards if c.id == deck_item.card_id), None)
            if card_obj:
                poke = self.pokemon_repo.get_by_id(card_obj.pokemon_id)
                if poke:
                    enriched_deck.append(
                        {
                            "id": poke.id,
                            "name": poke.name,
                            "move": poke.move,
                            "description": poke.description,
                        }
                    )

        return {
            "id": user.id,
            "username": user.username,
            "points": user.points,
            "rank": user.rank,
            "cards": enriched_collection,
            "deck": enriched_deck,
        }
