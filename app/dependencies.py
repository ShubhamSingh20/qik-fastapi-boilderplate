"""FastAPI dependency injection providers."""

from app.config import AuthConfig, DatabaseConfig
from app.db.sqlite import SQLiteDB
from app.service.auth import AuthService
from app.service.notes import NoteService

_db_instance: SQLiteDB | None = None


def get_db() -> SQLiteDB:
    """Shared SQLiteDB singleton."""
    global _db_instance
    if _db_instance is None:
        config = DatabaseConfig()
        _db_instance = SQLiteDB(config)
    return _db_instance


def get_auth_service() -> AuthService:
    return AuthService(db=get_db(), config=AuthConfig())


def get_note_service() -> NoteService:
    return NoteService(db=get_db())
