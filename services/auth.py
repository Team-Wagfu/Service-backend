"""
handle auth and registration services
"""

from sqlalchemy.orm import Session
from datetime import date

from schemas.user import createUser, readUser
from repo.user import UserRepository as repo
from core.exceptions import UserExistsError, AuthenticationError
from models.user import User
from services.security.helper import verify_password


class AuthService:
    @staticmethod
    def register(user: createUser, session: Session) -> readUser:
        # check if user exists
        if repo.user_exists(user.email, session):
            raise UserExistsError()

        from repo.profile import Profile as profile_repo

        db_user: User = repo.create_user(user, session)
        
        # Initialize the specific profile record
        profile_repo.create_default_profile(
            session=session,
            user_id=db_user.user_id,
            id=db_user.profile_id,
            user_type=db_user.type
        )
        
        session.commit()

        return readUser(
            name=db_user.display_name, email=db_user.email, profile_id=db_user.profile_id
        )

    @staticmethod
    def login(email: str, password: str, session: Session) -> readUser:
        """
        Authenticates a user, tracks login metrics, and returns client data.
        """
        try:
            db_user = repo.get_user_by_email(email, session)

            # Block login if user does not exist or has been soft-deleted
            if not db_user or not db_user.active:
                raise AuthenticationError()

            # Check password integrity
            if not verify_password(password, db_user.password_hash):
                raise AuthenticationError()

            # Record login datetime audit point
            db_user.last_login = date.today()
            session.commit()

            return readUser(
                name=db_user.display_name,
                email=db_user.email,
                profile_id=db_user.profile_id,
            )
        except Exception:
            session.rollback()
            raise AuthenticationError()
