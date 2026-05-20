from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.factories.card_factory import CardFactory
from app.infrastructure.repositories.card_repository import CardRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.jwt_handler import create_token
from app.infrastructure.security.password import hash_password
from app.shared.exceptions.domain_exception import DomainException


class RegisterUserUseCase:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.card_repo = CardRepository(db)
        self.card_factory = CardFactory(db)

    def execute(self, username: str, password: str) -> str:
        try:
            hashed_password = hash_password(password)
            user = self.user_repo.create(username, hashed_password)

            cards = self.card_factory.create_random_cards(owner_id=user.id, quantity=6)

            self.card_repo.create_many(cards)

            token = create_token(user.id)
            return token
        except IntegrityError:
            self.db.rollback()
            raise DomainException("Usuário já existe.") from None
