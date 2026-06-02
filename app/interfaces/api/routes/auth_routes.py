from fastapi import APIRouter

from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.register_user import RegisterUserUseCase
from app.interfaces.api.dependencies import DbSession, OAuth2Form
from app.schemas.auth_schema import (
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
def login(db: DbSession, form_data: OAuth2Form):
    use_case = LoginUserUseCase(db)
    token = use_case.execute(username=form_data.username, password=form_data.password)

    return {"message": "Login realizado com sucesso", "access_token": token}
