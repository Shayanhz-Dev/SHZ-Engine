from sqlalchemy.orm import Session

from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.service.password_service import PasswordService
from app.modules.users.service.user_service import UserService
from app.modules.users.service.token_service import TokenService

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