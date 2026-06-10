"""
CRUD operations for user creation/deletion/updation

NO COMMITS IN CRUD
"""

from random import randint
from uuid import uuid4
from sqlalchemy import select
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
        slug = ""
        id_num = str(randint(0, 99999)).zfill(5)
        if user.type == UserType.doctor:
            slug = "DOC"
        elif user.type == UserType.facilitator:
            slug = "FAC"
        elif user.type == UserType.owner:
            slug = "OWN"

        profile_id = f"{slug}-2026-{id_num}"

        # FIX: Changed from class-level reference 'createUser.pwd' to instance 'user.pwd'
        password_hash = hash_password(user.pwd)

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
    def get_user_id_by_profile_id(profile_id: str, session: Session):
        if not profile_id:
            return None

        stmt = select(User.user_id).where(User.profile_id == profile_id)
        return session.scalar(stmt)

    @staticmethod
    def get_user_by_email(user_email: str, session: Session) -> User | None:
        """Helper to retrieve a full User object by email for auth/update checks."""
        stmt = select(User).where(User.email == user_email)
        return session.scalar(stmt)

    @staticmethod
    def user_exists(user_email: str, session: Session) -> bool:
        stmt = select(User.email).where(User.email == user_email)
        return session.scalar(stmt) is not None

    @staticmethod
    def update_user(user: createUser, session: Session) -> User | None:
        """
        Updates user details based on incoming createUser schema.
        Assumes the email acts as the immutable look-up identifier.
        """
        db_user = UserRepository.get_user_by_email(user.email, session)
        if not db_user:
            return None

        db_user.display_name = user.name
        db_user.type = user.type

        # Only re-hash password if a new one is provided or explicitly matches validation
        if user.pwd:
            db_user.password_hash = hash_password(user.pwd)

        session.flush()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(email: str, session: Session) -> bool:
        """
        Executes a soft-delete by toggling the active flag to False,
        matching the cascading restoration logic specified in user models.
        """
        db_user = UserRepository.get_user_by_email(email, session)
        if db_user:
            db_user.active = False
            session.flush()
            return True
        return False
