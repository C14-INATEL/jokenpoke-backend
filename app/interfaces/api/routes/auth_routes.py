from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.register_user import RegisterUserUseCase
from app.infrastructure.db.session import get_db
from app.schemas.auth_schema import (
    LoginUserRequest,
    LoginUserResponse,
    RegisterUserRequest,
    RegisterUserResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterUserResponse)
def register(payload: RegisterUserRequest, db: Session = Depends(get_db)):
    # O Router delega a responsabilidade para o Use Case
    use_case = RegisterUserUseCase(db)

    # Executa a regra de negócio e recebe o token
    token = use_case.execute(username=payload.username, password=payload.password)

    return {"message": "Usuário registrado com sucesso", "access_token": token}


@router.post("/login", response_model=LoginUserResponse)
def login(payload: LoginUserRequest, db: Session = Depends(get_db)):
    use_case = LoginUserUseCase(db)
    token = use_case.execute(username=payload.username, password=payload.password)

    return {"message": "Login realizado com sucesso", "access_token": token}
