from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.infrastructure.repositories.ranking_repository import RankingRepository


class TestRankingRepository:
    def test_get_ranking_list_returns_query_result(self):
        db_mock = MagicMock(spec=Session)

        u1 = MagicMock()
        u1.points = 200
        u1.id = 1

        u2 = MagicMock()
        u2.points = 150
        u2.id = 2

        u3 = MagicMock()
        u3.points = 80
        u3.id = 3

        db_mock.query.return_value.order_by.return_value.all.return_value = [u1, u2, u3]

        repo = RankingRepository(db=db_mock)

        resultado = repo.get_ranking_list()

        assert resultado == [u1, u2, u3]

    def test_get_ranking_list_returns_users_sorted_by_points(self):
        db_mock = MagicMock(spec=Session)

        u1 = MagicMock()
        u1.points = 500
        u1.id = 10

        u2 = MagicMock()
        u2.points = 300
        u2.id = 5

        db_mock.query.return_value.order_by.return_value.all.return_value = [u1, u2]

        repo = RankingRepository(db=db_mock)

        resultado = repo.get_ranking_list()

        assert resultado[0] is u1
        assert resultado[1] is u2
        db_mock.query.return_value.order_by.assert_called_once()

    def test_get_ranking_list_empty_returns_empty(self):
        db_mock = MagicMock(spec=Session)
        db_mock.query.return_value.order_by.return_value.all.return_value = []

        repo = RankingRepository(db=db_mock)

        resultado = repo.get_ranking_list()

        assert isinstance(resultado, list)
        assert len(resultado) == 0

    def test_get_ranking_list_single_user_returns_one_user(self):
        db_mock = MagicMock(spec=Session)

        unico = MagicMock()
        unico.points = 42
        unico.id = 99

        db_mock.query.return_value.order_by.return_value.all.return_value = [unico]

        repo = RankingRepository(db=db_mock)

        resultado = repo.get_ranking_list()

        assert len(resultado) == 1
        assert resultado[0] is unico
