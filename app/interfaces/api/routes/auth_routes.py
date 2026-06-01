from fastapi import APIRouter

from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.register_user import RegisterUserUseCase
from app.interfaces.api.dependencies import DbSession
from app.infrastructure.db.session import get_db
from app.schemas.auth_schema import (
    LoginUserRequest,
    LoginUserResponse,
    RegisterUserRequest,
    RegisterUserResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterUserResponse)
def register(payload: RegisterUserRequest, db: DbSession):
    use_case = RegisterUserUseCase(db)

    token = use_case.execute(username=payload.username, password=payload.password)

    return {"message": "Usuário registrado com sucesso", "access_token": token}


@router.post("/login", response_model=LoginUserResponse)
def login(payload: LoginUserRequest, db: DbSession):
    use_case = LoginUserUseCase(db)
    token = use_case.execute(username=payload.username, password=payload.password)

    return {"message": "Login realizado com sucesso", "access_token": token}
