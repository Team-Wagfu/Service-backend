"""
engine creation and instance management
[global shared instance]
"""

import logging
from sqlalchemy import create_engine, text

from models.base import Base
from models.user import User
from models.profile import DoctorProfile, PetOwnerProfile, FacilitatorProfile
from models.pets import Pets, MedicalRecords, Vaccination

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


# create the required tables
Base.metadata.create_all(
    bind=engine,
    tables=[
        # user tables
        User.__table__,
        # profile tables
        DoctorProfile.__table__,
        PetOwnerProfile.__table__,
        FacilitatorProfile.__table__,
        # pets tables
    ],
)


def validate_engine():
    """invoke to test connectivity"""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


__all__ = ["engine", "validate_engine"]
