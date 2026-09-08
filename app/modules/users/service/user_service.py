from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.service.password_service import PasswordService
from app.modules.users.models.user import User
from app.modules.users.service.token_service import TokenService
from sqlalchemy.orm import Session

class UserService:
    def __init__(
            self,
            user_repository: UserRepository,
            password_service: PasswordService,
            token_service: TokenService,
            session: Session
            ):
        
        self.user_repository = user_repository
        self.password_service = password_service
        self.token_service = token_service
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

    def login(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password.")

        if not self.password_service.verify(password, user.password_hash):
            raise ValueError("Invalid email or password.")

        return self.token_service.create_token(user_id=user.id)
    