import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import settings

class TokenService:

    def create_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

        payload = {
            "sub": str(user_id),
            "exp": expire,
            }
        token = jwt.encode(
            payload,
            settings.secret_key,
            algorithm=settings.algorithm
        )

        return token

    def verify_token(self, token: str) -> dict:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        return payload