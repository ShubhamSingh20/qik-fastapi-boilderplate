"""Authentication service: JWT tokens and password hashing."""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext

from app.config import AuthConfig
from app.db.query.auth import AuthQuery
from app.db.sqlite import SQLiteDB

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: SQLiteDB, config: AuthConfig):
        self._query = AuthQuery(db)
        self._config = config

    async def authenticate(self, email: str, password: str) -> Optional[dict]:
        """Validate credentials. Returns user dict or None."""
        user = await self._query.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user["password_hash"]):
            return None
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[dict]:
        return await self._query.get_user_by_id(user_id)

    async def create_user(self, email: str, password: str) -> dict:
        """Hash password and insert a new user."""
        hashed = self.hash_password(password)
        return await self._query.create_user(email, hashed)

    def create_access_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self._config.access_token_expire_minutes
        )
        payload = {"sub": user_id, "exp": expire}
        return jwt.encode(payload, self._config.secret_key, algorithm=self._config.algorithm)

    def decode_token(self, token: str) -> Optional[int]:
        """Decode JWT and return user_id, or None if invalid/expired."""
        try:
            payload = jwt.decode(
                token, self._config.secret_key, algorithms=[self._config.algorithm]
            )
            return payload.get("sub")
        except jwt.PyJWTError:
            return None

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)
