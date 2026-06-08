"""
CRUD operations for user creation/deletion/updation

NO COMMITS IN CRUD
"""

from random import randint
from uuid import uuid4
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import createUser, readUser
from core.enums import UserType
from services.security.helper import hash_password


class UserRepository:
    @staticmethod
    def create_user(user: createUser, session: Session) -> User:

        # create the user uuid
        user_uuid = uuid4()

        # type of user
        # inferred from createUser model
        user_type = user.type

        # display name
        # inferred from createUser model
        display_name = user.name

        # email
        # inferred from createUser model
        email = user.email

        # profile id
        # find the last number for the corresponding id slug
        # for the time being, use random numbers
        id_num = str(randint(0, 99999)).zfill(5)
        if user.type == UserType.doctor:
            slug = "DOC"
        elif user.type == UserType.facilitator:
            slug = "FAC"
        elif user.type == UserType.owner:
            slug = "OWN"

        profile_id = f"{slug}-2026-{id_num}"

        password_hash = hash_password(createUser.pwd)

        info = User(
            user_id=user_uuid,
            type=user_type,
            display_name=display_name,
            email=email,
            profile_id=profile_id,
            password_hash=password_hash,
        )

        session.add(info)
        session.flush()

        session.refresh(info)

        return info

    @staticmethod
    def user_exists(user_email: str, session: Session):
        stmt = select(User.email).where(User.email == user_email)
        return session.scalar(stmt) is not None

    @staticmethod
    def update_user(user: createUser, session: Session) -> User:
        pass

    @staticmethod
    def delete_user(email: str, session: Session):
        stmt = delete(User).where(User.email == email)
        session.execute(stmt)
