"""
Authentication and token distribution

handle authentication
handle user registration
handle user deletion

token are always received through bearer
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, status, Depends
from fastapi.responses import Response

from schemas.user import createUser, readUser, loginUser
from services.jwt.master import user_metadata
from services.jwt.helper import create_jwt
from db.dependencies import get_db
from services.auth import AuthService
from models.user import User
from sqlalchemy import select

# configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("Starting /user router")
router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/create", response_model=readUser, status_code=status.HTTP_201_CREATED)
async def create_user(
    userData: Annotated[createUser, Body(...)],
    response: Response,
    session: Session = Depends(get_db),
):

    # handle user creation
    logger.debug(
        """creating user:
        [+] username    %s
        [+] email       %s
        [*] passwd      %s
    """,
        userData.name,
        userData.email,
        userData.pwd,
    )

    # Use AuthService to register the user in the DB
    registered_user = AuthService.register(userData, session)
    profile_type: str = userData.type.value
    profile_id: str = registered_user.profile_id

    now = datetime.now(timezone.utc)

    token: str = create_jwt(
        {
            "name": registered_user.name,
            "exp": int((now + timedelta(days=7)).timestamp()),
            "iat": int(now.timestamp()),
            "role": profile_type,  # fac, doc, own
            "profile_id": profile_id,
        }
    )
    logger.debug("creating token %s", token)

    logger.debug(
        """data:
        [+] token       %s
        [+] profile_id  %s
    """,
        token,
        profile_id,
    )

    response.set_cookie(key="Bearer", value=token, httponly=True)
    return registered_user


@router.post("/update", response_model=readUser, status_code=status.HTTP_200_OK)
async def update_user(
    userData: Annotated[createUser, Body(...)],
    response: Response,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    from repo.user import UserRepository
    from core.exceptions import AuthenticationError

    db_user = UserRepository.update_user(userData, session)
    if not db_user:
        raise AuthenticationError()

    session.commit()

    now = datetime.now(timezone.utc)
    token: str = create_jwt(
        {
            "name": db_user.display_name,
            "exp": int((now + timedelta(days=7)).timestamp()),
            "iat": int(now.timestamp()),
            "role": db_user.type.value,
            "profile_id": db_user.profile_id,
        }
    )
    response.set_cookie(key="Bearer", value=token, httponly=True)

    return readUser(
        name=db_user.display_name,
        email=db_user.email,
        profile_id=db_user.profile_id,
    )


# since only a logged in user can delete their account
# the account information shall be identified from the token
@router.delete("/delete", status_code=status.HTTP_200_OK, response_class=Response)
async def delete_user(
    response: Response,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    profile_id = user.get("profile_id")
    if not profile_id:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Profile ID not found in token")

    # Soft-delete the user
    stmt = select(User).where(User.profile_id == profile_id)
    db_user = session.scalar(stmt)
    if db_user:
        db_user.active = False

    # Delete the profile
    from repo.profile import Profile
    try:
        Profile.delete_profile(session, profile_id)
    except Exception as e:
        logger.error(f"Failed to delete profile: {e}")

    session.commit()

    logger.debug(
        """deleting user:
        [+] profile_id %s""",
        profile_id,
    )

    response.delete_cookie(
        "Bearer",
    )

    return Response(status_code=200, content="User deleted successfully")


@router.post("/login", response_model=readUser, status_code=status.HTTP_200_OK)
async def login_user(
    credentials: Annotated[loginUser, Body(...)],
    response: Response,
    session: Session = Depends(get_db),
):
    # Authenticate the user
    user_data = AuthService.login(credentials.email, credentials.pwd, session)

    # Determine user role from profile_id prefix
    profile_id = user_data.profile_id
    prefix = profile_id.split("-")[0] if profile_id else ""
    if prefix == "DOC":
        role = "doctor"
    elif prefix == "FAC":
        role = "fac"
    elif prefix == "OWN":
        role = "owner"
    else:
        role = ""

    now = datetime.now(timezone.utc)
    token: str = create_jwt(
        {
            "name": user_data.name,
            "exp": int((now + timedelta(days=7)).timestamp()),
            "iat": int(now.timestamp()),
            "role": role,
            "profile_id": profile_id,
        }
    )
    logger.debug("creating token %s", token)

    response.set_cookie(key="Bearer", value=token, httponly=True)
    return user_data


# logout
@router.post("/logout", status_code=status.HTTP_200_OK, response_class=Response)
async def logout_user(response: Response, user=Depends(user_metadata)):

    logger.debug(
        """logging out user:
        [+] profile_id %s""",
        user.get("profile_id"),
    )

    response.delete_cookie(
        "Bearer",
    )

    return Response(status_code=200, content="Logout successful")
