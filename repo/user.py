"""
CRUD operations for user creation/deletion/updation
"""

from sqlalchemy.orm import Session
from schemas.user import User as user_schema
from models.user import User as user_model


def create_user(data: user_schema, session: Session):
    Session
