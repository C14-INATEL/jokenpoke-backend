from sqlalchemy.orm import Session

from app.infrastructure.repositories.ranking_repository import RankingRepository


class GetRankingUseCase:
    def __init__(self, db: Session):
        self.ranking_repo = RankingRepository(db)

    def execute(self) -> list[dict]:
        users = self.ranking_repo.get_ranking_list()

        return [
            {
                "position": index,
                "username": user.username,
                "points": user.points,
                "rank": user.rank,
            }
            for index, user in enumerate(users, start=1)
        ]
