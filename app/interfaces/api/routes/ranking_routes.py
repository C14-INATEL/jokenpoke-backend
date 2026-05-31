from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.use_cases.get_ranking import GetRankingUseCase
from app.infrastructure.db.session import get_db
from app.schemas.ranking_schema import RankingResponse

router = APIRouter(prefix="/ranking", tags=["Ranking"])


@router.get("/", response_model=list[RankingResponse])
def get_ranking(db: Session = Depends(get_db)):
    use_case = GetRankingUseCase(db)
    return use_case.execute()
