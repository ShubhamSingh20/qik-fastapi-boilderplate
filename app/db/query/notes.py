"""SQL queries for notes."""

from typing import Optional

SELECT_NOTES_BY_USER = """
SELECT id, user_id, title, content, created_at, updated_at
FROM notes WHERE user_id = ? ORDER BY created_at DESC
"""

SELECT_NOTE_BY_ID = """
SELECT id, user_id, title, content, created_at, updated_at
FROM notes WHERE id = ? AND user_id = ?
"""

INSERT_NOTE = """
INSERT INTO notes (user_id, title, content)
VALUES (?, ?, ?)
"""

UPDATE_NOTE = """
UPDATE notes SET title = ?, content = ?, updated_at = datetime('now')
WHERE id = ? AND user_id = ?
"""

DELETE_NOTE = """
DELETE FROM notes WHERE id = ? AND user_id = ?
"""


class NoteQuery:
    def __init__(self, db):
        self._db = db

    async def get_notes_by_user(self, user_id: int) -> list[dict]:
        rows = await self._db.select_many(SELECT_NOTES_BY_USER, (user_id,))
        return [self._row_to_dict(row) for row in rows]

    async def get_note_by_id(self, note_id: int, user_id: int) -> Optional[dict]:
        row = await self._db.select_one(SELECT_NOTE_BY_ID, (note_id, user_id))
        return self._row_to_dict(row) if row else None

    async def create_note(self, user_id: int, title: str, content: str) -> dict:
        lastrowid = await self._db.insert(INSERT_NOTE, (user_id, title, content))
        return await self.get_note_by_id(lastrowid, user_id)

    async def update_note(self, note_id: int, user_id: int, title: str, content: str) -> Optional[dict]:
        await self._db.update_delete(UPDATE_NOTE, (title, content, note_id, user_id))
        return await self.get_note_by_id(note_id, user_id)

    async def delete_note(self, note_id: int, user_id: int) -> int:
        return await self._db.update_delete(DELETE_NOTE, (note_id, user_id))

    @staticmethod
    def _row_to_dict(row: dict) -> Optional[dict]:
        if not row:
            return None
        return {
            "id": row["id"],
            "user_id": row["user_id"],
            "title": row["title"],
            "content": row["content"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
