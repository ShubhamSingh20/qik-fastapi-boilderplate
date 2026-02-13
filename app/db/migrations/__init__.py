"""Migration runner for SQLite."""

from pathlib import Path


def get_migration_files() -> list[Path]:
    """Return sorted list of .sql migration files."""
    migration_dir = Path(__file__).parent
    return sorted(migration_dir.glob("*.sql"))
