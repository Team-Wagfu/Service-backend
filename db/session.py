"""sessionmaker configuration and setup"""

from sqlalchemy.orm import sessionmaker
from db.engine import engine

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)

__all__ = ["SessionLocal"]

# sampleuser.taken@gmail.com
# RandomWords
