"""SQL queries for user authentication."""

from typing import Optional

SELECT_USER_BY_EMAIL = """
SELECT id, email, password_hash, created_at, updated_at
FROM users WHERE email = ?
"""

SELECT_USER_BY_ID = """
SELECT id, email, password_hash, created_at, updated_at
FROM users WHERE id = ?
"""

INSERT_USER = """
INSERT INTO users (email, password_hash)
VALUES (?, ?)
"""


class AuthQuery:
    def __init__(self, db):
        self._db = db

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        row = await self._db.select_one(SELECT_USER_BY_EMAIL, (email,))
        return self._row_to_dict(row) if row else None

    async def get_user_by_id(self, user_id: int) -> Optional[dict]:
        row = await self._db.select_one(SELECT_USER_BY_ID, (user_id,))
        return self._row_to_dict(row) if row else None

    async def create_user(self, email: str, password_hash: str) -> dict:
        lastrowid = await self._db.insert(INSERT_USER, (email, password_hash))
        return await self.get_user_by_id(lastrowid)

    @staticmethod
    def _row_to_dict(row: dict) -> Optional[dict]:
        if not row:
            return None
        return {
            "id": row["id"],
            "email": row["email"],
            "password_hash": row["password_hash"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
