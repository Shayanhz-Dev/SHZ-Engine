from app.modules.users.repositories import user_repository
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.service import password_service
from app.modules.users.service.password_service import PasswordService
from app.modules.users.models.user import User
from sqlalchemy.orm import Session

class UserService:
    def __init__(
            self,
            user_repository: UserRepository,
            password_service: PasswordService,
            session: Session
            ):
        
        self.user_repository = user_repository
        self.password_service = password_service
        self.session = session

    def register(
        self,
        email: str,
        password: str,
        full_name: str
    ) -> User:

        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists.")

        password_hash = self.password_service.hash(password)

        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name)

        try:
            user = self.user_repository.create(user)
            self.session.commit()
            return user
        except Exception:
            self.session.rollback()
            raise