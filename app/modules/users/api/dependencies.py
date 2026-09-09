from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.service.password_service import PasswordService
from app.modules.users.service.user_service import UserService
from app.modules.users.service.token_service import TokenService
from fastapi import Depends, status, HTTPException
import jwt
from app.db.session import get_db
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_user_service(session: Session) -> UserService:
    user_repository = UserRepository(session)
    password_service = PasswordService()
    token_service = TokenService()
    return UserService(
        session=session,
        user_repository=user_repository,
        password_service=password_service,
        token_service=token_service,
    )

def get_token(
        token: str = Depends(oauth2_scheme),
) -> str:
    return token

def get_current_user(
    token: str = Depends(get_token),
    session: Session = Depends(get_db),
):
    token_service = TokenService()
    user_repository = UserRepository(session)

    try:
        payload = token_service.verify_token(token)
    except jwt.invalid_token_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user = user_repository.get_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user_id