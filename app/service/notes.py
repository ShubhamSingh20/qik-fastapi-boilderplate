"""Notes service."""

from typing import Optional

from app.db.query.notes import NoteQuery
from app.db.sqlite import SQLiteDB


class NoteService:
    def __init__(self, db: SQLiteDB):
        self._query = NoteQuery(db)

    async def list_notes(self, user_id: int) -> list[dict]:
        return await self._query.get_notes_by_user(user_id)

    async def get_note(self, note_id: int, user_id: int) -> Optional[dict]:
        return await self._query.get_note_by_id(note_id, user_id)

    async def create_note(self, user_id: int, title: str, content: str) -> dict:
        return await self._query.create_note(user_id, title, content)

    async def update_note(
        self, note_id: int, user_id: int, title: str = None, content: str = None
    ) -> Optional[dict]:
        """Partial update -- keeps existing values for fields not provided."""
        existing = await self._query.get_note_by_id(note_id, user_id)
        if not existing:
            return None
        final_title = title if title is not None else existing["title"]
        final_content = content if content is not None else existing["content"]
        return await self._query.update_note(note_id, user_id, final_title, final_content)

    async def delete_note(self, note_id: int, user_id: int) -> bool:
        rows = await self._query.delete_note(note_id, user_id)
        return rows > 0
