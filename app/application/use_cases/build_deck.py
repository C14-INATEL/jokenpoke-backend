from sqlalchemy.orm import Session
from app.infrastructure.repositories.deck_repository import DeckRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.shared.exceptions.domain_exception import DomainException
from app.shared.exceptions.not_found_exception import NotFoundException

class BuildDeckUseCase:
    def __init__(self, db: Session):
        self.deck_repo = DeckRepository(db)
        self.user_repo = UserRepository(db)

    def execute(self, user_id: int, pokemon_ids: list[int]) -> str:
        user = self.user_repo.get_by_id_with_relations(user_id)
        if not user:
            raise NotFoundException(f"Usuário com ID {user_id} não encontrado.")

        available_cards = list(user.cards) 
        selected_card_ids = []

        for p_id in pokemon_ids:
            card_match = next((c for c in available_cards if c.pokemon_id == p_id), None)
            
            if not card_match:
                raise DomainException(f"Você não possui o pokémon de ID {p_id}.")
            
            selected_card_ids.append(card_match.id)
            available_cards.remove(card_match)

        self.deck_repo.clear_user_deck(user_id)
        self.deck_repo.save_deck(user_id, selected_card_ids)

        return user.username