"""
handle auth and registration services
"""

from sqlalchemy.orm import Session

from schemas.user import createUser, readUser
from repo.user import UserRepository as repo
from core.exceptions import UserExistsError, AuthenticationError
from models.user import User


class AuthService:
    @staticmethod
    def register(user: createUser, session: Session):

        # check if user exists
        if repo.user_exists(user.email, session):
            raise UserExistsError()

        try:
            data: User = repo.create_user(user, session)
            session.commit()
        except:
            session.rollback()
            raise AuthenticationError()
        finally:
            session.close()

    @staticmethod
    def login()