"""Async SQLite database wrapper."""

import logging
from typing import Any, Optional

import aiosqlite

from app.config import DatabaseConfig

logger = logging.getLogger(__name__)


class SQLiteDB:
    def __init__(self, config: DatabaseConfig):
        self._path = config.path
        self._conn: Optional[aiosqlite.Connection] = None

    async def init(self):
        """Open connection, enable WAL + foreign keys, run migrations."""
        self._conn = await aiosqlite.connect(self._path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute("PRAGMA journal_mode=WAL")
        await self._conn.execute("PRAGMA foreign_keys=ON")
        await self._run_migrations()
        logger.info("Database initialised: %s", self._path)

    async def close(self):
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def _run_migrations(self):
        from app.db.migrations import get_migration_files

        for migration_file in get_migration_files():
            sql_content = migration_file.read_text()
            for raw in sql_content.split(";"):
                stmt = raw.strip()
                if stmt and not stmt.startswith("--"):
                    await self._conn.execute(stmt + ";")
        await self._conn.commit()
        logger.info("Migrations complete")

    async def execute(self, sql: str, params: tuple = ()) -> aiosqlite.Cursor:
        """Execute a statement and commit."""
        cursor = await self._conn.execute(sql, params)
        await self._conn.commit()
        return cursor

    async def select_one(self, sql: str, params: tuple = ()) -> Optional[dict]:
        """Return a single row as a dict, or None."""
        cursor = await self._conn.execute(sql, params)
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def select_many(self, sql: str, params: tuple = ()) -> list[dict]:
        """Return all matching rows as a list of dicts."""
        cursor = await self._conn.execute(sql, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def insert(self, sql: str, params: tuple = ()) -> Optional[int]:
        """Insert a row and return lastrowid."""
        cursor = await self._conn.execute(sql, params)
        await self._conn.commit()
        return cursor.lastrowid

    async def update_delete(self, sql: str, params: tuple = ()) -> int:
        """Run an UPDATE or DELETE and return affected row count."""
        cursor = await self._conn.execute(sql, params)
        await self._conn.commit()
        return cursor.rowcount
