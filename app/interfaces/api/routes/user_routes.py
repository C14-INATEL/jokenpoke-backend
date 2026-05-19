from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.use_cases.delete_user import DeleteUserUseCase
from app.application.use_cases.get_all_users import GetAllUsersUseCase
from app.application.use_cases.get_user_by_id import GetUserByIdUseCase
from app.infrastructure.db.session import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model_exclude={
        "__all__": {
            "collection": {"__all__": {"description"}},
            "deck": {"__all__": {"description"}},
        }
    },
)
def get_all_users(db: Session = Depends(get_db)):
    use_case = GetAllUsersUseCase(db)
    users = use_case.execute()

    return users


@router.get(
    "/{user_id}",
    response_model_exclude={
        "collection": {"__all__": {"description"}},
        "deck": {"__all__": {"description"}},
    },
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    use_case = GetUserByIdUseCase(db)
    return use_case.execute(user_id)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    use_case = DeleteUserUseCase(db)
    deleted_username = use_case.execute(user_id)

    return {"message": f"Usuário {deleted_username} deletado com sucesso"}
