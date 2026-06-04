from types import SimpleNamespace
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.infrastructure.repositories.user_repository import UserRepository


class TestUserRepositoryUpdateRanking:
    def test_update_ranking_updates_rank_and_points(self):
        db_mock = MagicMock(spec=Session)
        user = SimpleNamespace(id=1, rank="Beginner", points=10)
        db_mock.query.return_value.filter_by.return_value.first.return_value = user

        repo = UserRepository(db=db_mock)

        result = repo.update_ranking(user_id=1, rank="Great", points=5)

        assert result is user
        assert user.rank == "Great"
        assert user.points == 5
        db_mock.query.return_value.filter_by.assert_called_once_with(id=1)
        db_mock.commit.assert_called_once()
        db_mock.refresh.assert_called_once_with(user)

    def test_update_ranking_returns_none_when_user_not_found(self):
        db_mock = MagicMock(spec=Session)
        db_mock.query.return_value.filter_by.return_value.first.return_value = None

        repo = UserRepository(db=db_mock)

        result = repo.update_ranking(user_id=999, rank="Great", points=5)

        assert result is None
        db_mock.commit.assert_not_called()
        db_mock.refresh.assert_not_called()
