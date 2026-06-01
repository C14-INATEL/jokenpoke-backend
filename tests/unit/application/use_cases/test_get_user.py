from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.application.use_cases.get_all_users import GetAllUsersUseCase
from app.application.use_cases.get_user_by_id import GetUserByIdUseCase
from app.shared.exceptions.not_found_exception import NotFoundException


class TestGetUserByIdUseCase:
    def test_get_user_by_id_mock_success(
        self,
        charizard_pokemon,
        pikachu_pokemon,
    ):
        db_mock = MagicMock(spec=Session)

        use_case = GetUserByIdUseCase(db=db_mock)

        use_case.user_repo = MagicMock()
        use_case.pokemon_repo = MagicMock()

        carta1 = SimpleNamespace(
            id=101,
            pokemon_id=charizard_pokemon.id,
        )

        carta2 = SimpleNamespace(
            id=102,
            pokemon_id=pikachu_pokemon.id,
        )

        deck_item = SimpleNamespace(card_id=101)

        usuario_falso = SimpleNamespace(
            id=10,
            username="Ash Ketchum",
            cards=[carta1, carta2],
            deck=[deck_item],
            points=100,
            position=1,
        )

        use_case.user_repo.get_by_id_with_relations.return_value = usuario_falso

        use_case.pokemon_repo.get_by_id.side_effect = lambda pokemon_id: {
            charizard_pokemon.id: charizard_pokemon,
            pikachu_pokemon.id: pikachu_pokemon,
        }.get(pokemon_id)

        resultado = use_case.execute(user_id=10)

        assert resultado["id"] == 10
        assert resultado["username"] == "Ash Ketchum"
        assert resultado["points"] == 100
        assert resultado["position"] == 1

        assert len(resultado["cards"]) == 2

        assert resultado["cards"][0]["name"] == "Charizard"
        assert resultado["cards"][1]["name"] == "Pikachu"

        assert len(resultado["deck"]) == 1
        assert resultado["deck"][0]["name"] == "Charizard"

        use_case.user_repo.get_by_id_with_relations.assert_called_once_with(10)

    def test_get_user_by_id_not_found_mock(self):
        db_mock = MagicMock(spec=Session)

        use_case = GetUserByIdUseCase(db=db_mock)

        use_case.user_repo = MagicMock()

        use_case.user_repo.get_by_id_with_relations.return_value = None

        with pytest.raises(NotFoundException):
            use_case.execute(user_id=999)


class TestGetAllUsersUseCase:
    def test_get_all_users_mock(self):
        db_mock = MagicMock(spec=Session)

        use_case = GetAllUsersUseCase(db=db_mock)

        use_case.user_repo = MagicMock()
        use_case.pokemon_repo = MagicMock()

        u1 = SimpleNamespace(
            id=1,
            username="Red",
            cards=[],
            deck=[],
            points=0,
            position=None,
        )

        u2 = SimpleNamespace(
            id=2,
            username="Blue",
            cards=[],
            deck=[],
            points=0,
            position=None,
        )

        use_case.user_repo.get_all_with_relations.return_value = [
            u1,
            u2,
        ]

        resultado = use_case.execute()

        assert isinstance(resultado, list)
        assert len(resultado) == 2

        assert resultado[0]["id"] == 1
        assert resultado[0]["username"] == "Red"

        assert resultado[1]["id"] == 2
        assert resultado[1]["username"] == "Blue"

        use_case.user_repo.get_all_with_relations.assert_called_once()
