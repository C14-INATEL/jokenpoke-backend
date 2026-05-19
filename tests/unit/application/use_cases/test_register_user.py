from unittest.mock import MagicMock, call, patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.application.use_cases.register_user import RegisterUserUseCase
from app.shared.exceptions.domain_exception import DomainException


def test_register_user_success_mock():

    db_mock = MagicMock()
    use_case = RegisterUserUseCase(db_mock)

    user_mock = MagicMock()
    user_mock.id = 123

    cards_mock = ["card1", "card2", "card3", "card4", "card5", "card6"]

    with (
        patch("app.application.use_cases.register_user.hash_password") as mock_hash,
        patch("app.application.use_cases.register_user.create_token") as mock_token,
    ):
        use_case.user_repo = MagicMock()
        use_case.card_repo = MagicMock()
        use_case.card_factory = MagicMock()

        mock_hash.return_value = "hashed_password"
        use_case.user_repo.create.return_value = user_mock
        use_case.card_factory.create_random_cards.return_value = cards_mock
        mock_token.return_value = "fake_jwt_token"

        tracker = MagicMock()

        def hash_side_effect(password):
            tracker.hash_password(password)
            return "hashed_password"

        def create_user_side_effect(u, p):
            tracker.user_repo.create(u, p)
            return user_mock

        def cards_side_effect(owner_id, quantity):
            tracker.card_factory.create_random_cards(
                owner_id=owner_id, quantity=quantity
            )
            return cards_mock

        def create_many_side_effect(cards):
            tracker.card_repo.create_many(cards)

        mock_hash.side_effect = hash_side_effect
        use_case.user_repo.create.side_effect = create_user_side_effect
        use_case.card_factory.create_random_cards.side_effect = cards_side_effect
        use_case.card_repo.create_many.side_effect = create_many_side_effect

        def token_side_effect(user_id):
            tracker.create_token(user_id)
            return "fake_jwt_token"

        mock_token.side_effect = token_side_effect

        result = use_case.execute("maria", "123456")

        assert result == "fake_jwt_token"

        expected_calls = [
            call.hash_password("123456"),
            call.user_repo.create("maria", "hashed_password"),
            call.card_factory.create_random_cards(owner_id=123, quantity=6),
            call.card_repo.create_many(cards_mock),
            call.create_token(123),
        ]

        assert tracker.mock_calls == expected_calls


def test_register_user_duplicate_mock():

    db_mock = MagicMock()
    use_case = RegisterUserUseCase(db_mock)

    with patch("app.application.use_cases.register_user.hash_password") as mock_hash:
        use_case.user_repo = MagicMock()

        mock_hash.return_value = "hashed_password"
        use_case.user_repo.create.side_effect = IntegrityError(
            statement=None, params=None, orig=None
        )

        with pytest.raises(DomainException) as exc:
            use_case.execute("maria", "123456")

        assert str(exc.value) == "Usuário já existe."

        db_mock.rollback.assert_called_once()
