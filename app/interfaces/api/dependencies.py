from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.infrastructure.security.auth_dependencies import get_current_user_id

DbSession = Annotated[Session, Depends(get_db)]

CurrentUser = Annotated[int, Depends(get_current_user_id)]

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
