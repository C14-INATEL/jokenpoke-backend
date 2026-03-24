from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.password import hash_password
from app.infrastructure.security.jwt_handler import create_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    user = repo.create(username, hash_password(password))

    token = create_token(user.id)

    return {"access_token": token}