"""CLI script to create a user.

Usage:
    python -m cmd.create_user --email user@example.com --password secret
"""

import argparse
import asyncio
import os
import sys

# Allow running from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import AuthConfig, DatabaseConfig
from app.db.sqlite import SQLiteDB
from app.service.auth import AuthService


async def main():
    parser = argparse.ArgumentParser(description="Create a new user")
    parser.add_argument("--email", required=True, help="User email")
    parser.add_argument("--password", required=True, help="User password")
    args = parser.parse_args()

    db = SQLiteDB(DatabaseConfig())
    await db.init()

    try:
        auth = AuthService(db=db, config=AuthConfig())
        user = await auth.create_user(args.email, args.password)
        print(f"User created: {user['id']} ({user['email']})")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
