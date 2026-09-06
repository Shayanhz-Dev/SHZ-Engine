from sqlalchemy.orm import Session
from sqlalchemy import select
from app.modules.users.models.user import User

class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)

        result = self.session.execute(query)

        return result.scalar_one_or_none()

    def get_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        result = self.session.execute(query)

        return result.scalar_one_or_none()

    def create(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.flush()
            self.session.refresh(user)
            return user
        except Exception:
            self.session.rollback()
            raise

    def delete(self, user: User) -> None:
        try:
            self.session.delete(user)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
