from fastapi import APIRouter

from app.application.use_cases.register_user import RegisterUserUseCase
from app.interfaces.api.dependencies import DbSession
from app.schemas.auth_schema import RegisterUserRequest, RegisterUserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterUserResponse)
def register(payload: RegisterUserRequest, db: DbSession):
    use_case = RegisterUserUseCase(db)

    token = use_case.execute(username=payload.username, password=payload.password)

    return {"message": "Usuário registrado com sucesso", "access_token": token}
