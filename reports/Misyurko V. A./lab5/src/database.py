"""Database configuration for the computer firm project."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'computer_firm.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SESSION_LOCAL = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Base class for ORM models."""

    def as_dict(self) -> dict[str, object]:
        """Return the model fields as a plain dictionary."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def get_primary_key(self) -> object:
        """Return the value of the primary key."""
        return getattr(self, "id", None)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for FastAPI dependencies."""
    database = SESSION_LOCAL()
    try:
        yield database
    finally:
        database.close()
