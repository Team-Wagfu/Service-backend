"""
engine creation and instance management
[global shared instance]
"""

import logging
from sqlalchemy import create_engine, text

from config import config

# setup logging
logger = logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


engine = create_engine(
    config.url,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False,
    logging_name="MainEngine",
    pool_logging_name="MainPool",
)


def validate_engine():
    """invoke to test connectivity"""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


__all__ = ["engine", "validate_engine"]
