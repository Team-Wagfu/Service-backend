"""
define dependencies for retrieving db instance
"""

from collections.abc import Generator
from sqlalchemy.orm import Session
from db.session import SessionLocal


def get_db() -> Generator:
    """dependency to get db session and cleanup after request teardown"""
    instance: Session = SessionLocal()

    try:
        yield instance
    finally:
        instance.close()


__all__ = ["get_db"]
