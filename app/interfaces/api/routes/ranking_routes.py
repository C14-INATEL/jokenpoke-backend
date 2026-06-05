from fastapi import APIRouter

from app.application.use_cases.get_ranking import GetRankingUseCase
from app.interfaces.api.dependencies import DbSession
from app.schemas.ranking_schema import RankingResponse

router = APIRouter(prefix="/ranking", tags=["Ranking"])


@router.get("/", response_model=list[RankingResponse])
def get_ranking(db: DbSession):
    use_case = GetRankingUseCase(db)
    return use_case.execute()
