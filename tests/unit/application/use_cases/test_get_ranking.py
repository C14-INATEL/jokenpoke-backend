from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.application.use_cases.get_ranking import GetRankingUseCase


class TestGetRankingUseCase:
    def test_execute_returns_list_of_dicts(self):
        # Arrange
        db_mock = MagicMock(spec=Session)
        use_case = GetRankingUseCase(db=db_mock)
        use_case.ranking_repo = MagicMock()

        usuario = MagicMock()
        usuario.username = "Ash"
        usuario.points = 100
        usuario.rank = "Beginner"

        use_case.ranking_repo.get_ranking_list.return_value = [usuario]

        # Act
        resultado = use_case.execute()

        # Assert
        assert isinstance(resultado, list)
        assert len(resultado) == 1
        assert resultado[0]["position"] == 1
        assert resultado[0]["username"] == "Ash"
        assert resultado[0]["points"] == 100
        assert resultado[0]["rank"] == "Beginner"

    def test_execute_with_multiple_users(self):
        # Arrange
        db_mock = MagicMock(spec=Session)
        use_case = GetRankingUseCase(db=db_mock)
        use_case.ranking_repo = MagicMock()

        u1 = MagicMock()
        u1.username = "Red"
        u1.points = 200
        u1.rank = "Expert"

        u2 = MagicMock()
        u2.username = "Blue"
        u2.points = 150
        u2.rank = "Intermediate"

        u3 = MagicMock()
        u3.username = "Gary"
        u3.points = 80
        u3.rank = "Beginner"

        use_case.ranking_repo.get_ranking_list.return_value = [u1, u2, u3]

        # Act
        resultado = use_case.execute()

        # Assert
        assert len(resultado) == 3
        assert resultado[0]["position"] == 1
        assert resultado[0]["username"] == "Red"
        assert resultado[1]["position"] == 2
        assert resultado[1]["username"] == "Blue"
        assert resultado[2]["position"] == 3
        assert resultado[2]["username"] == "Gary"

    def test_execute_with_empty_list(self):
        # Arrange
        db_mock = MagicMock(spec=Session)
        use_case = GetRankingUseCase(db=db_mock)
        use_case.ranking_repo = MagicMock()

        use_case.ranking_repo.get_ranking_list.return_value = []

        # Act
        resultado = use_case.execute()

        # Assert
        assert isinstance(resultado, list)
        assert len(resultado) == 0

    def test_execute_calls_get_ranking_list(self):
        # Arrange
        db_mock = MagicMock(spec=Session)
        use_case = GetRankingUseCase(db=db_mock)
        use_case.ranking_repo = MagicMock()

        use_case.ranking_repo.get_ranking_list.return_value = []

        # Act
        use_case.execute()

        # Assert
        use_case.ranking_repo.get_ranking_list.assert_called_once()

    def test_execute_returns_required_fields(self):
        # Arrange: garante que apenas position, username e points são retornados
        db_mock = MagicMock(spec=Session)
        use_case = GetRankingUseCase(db=db_mock)
        use_case.ranking_repo = MagicMock()

        usuario = MagicMock()
        usuario.username = "Pikachu"
        usuario.points = 999
        usuario.rank = "Master"

        use_case.ranking_repo.get_ranking_list.return_value = [usuario]

        # Act
        resultado = use_case.execute()

        # Assert
        assert set(resultado[0].keys()) == {"position", "username", "points", "rank"}
