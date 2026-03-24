from app.domain.entities.user import User
from app.domain.factories.card_factory import CardFactory


class RegisterUserUseCase:

    def __init__(self):
        self.card_factory = CardFactory()

    def execute(self, user_id: int, username: str) -> tuple[User, list]:

        user = User(id=user_id, username=username)

        cards = self.card_factory.create_random_cards(
            owner_id=user_id,
            quantity=6
        )

        return user, cards