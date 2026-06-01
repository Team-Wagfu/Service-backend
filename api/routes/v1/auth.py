"""
Authentication and token distribution

handle authentication
handle user registration
handle user deletion

token are always received through bearer
"""

import logging
from typing import Annotated
from fastapi import APIRouter, Body, status, Depends
from fastapi.responses import Response
from datetime import datetime, timedelta, timezone

from schemas.user import createUser, loginUser, readUser
from core.enums import UserType
from services.jwt.master import user_metadata
from services.jwt.helper import create_jwt

logger = logging.getLogger(__name__)

logger.info("Starting /user router")
router = APIRouter(prefix="/user", tags=["user", "registration"])


def _profile_id_for(user_type: UserType) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    if user_type == UserType.doctor:
        return f"DOC-{timestamp}"
    if user_type == UserType.facilitator:
        return f"CLN-{timestamp}"
    return f"PW-{timestamp}"


def _issue_token(name: str, profile_type: str, profile_id: str) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(days=7)
    return create_jwt(
        {
            "name": name,
            "exp": int(expiry.timestamp()),
            "profile_type": profile_type,
            "profile_id": profile_id,
        }
    )


@router.post("/create", response_model=readUser, status_code=status.HTTP_201_CREATED)
async def create_user(userData: Annotated[createUser, Body(...)], response: Response):

    # handle user creation
    logger.debug(f"""creating user:
        [+] username    {userData.name}
        [+] email       {userData.email}
        [*] passwd      {userData.pwd}
    """)

    # token creation and profile_id grepping

    profile_type: str = userData.type.value
    profile_id: str = _profile_id_for(userData.type)
    token: str = _issue_token(userData.name, profile_type, profile_id)
    logger.debug(f"creating token {token}")

    logger.debug(f"""data:
        [+] token       {token}
        [+] profile_id  {profile_id}
    """)

    response.set_cookie(key="Bearer Token", value=token, httponly=True)

    return readUser(
        name=userData.name,
        email=userData.email,
        profile_id=profile_id,
        profile_type=profile_type,
        token=token,
    )


@router.post("/login", response_model=readUser, status_code=status.HTTP_200_OK)
async def login_user(credentials: Annotated[loginUser, Body(...)], response: Response):
    profile_type = UserType.owner.value
    profile_id = _profile_id_for(UserType.owner)
    name = credentials.email.split("@")[0]
    token = _issue_token(name, profile_type, profile_id)

    response.set_cookie(key="Bearer Token", value=token, httponly=True)

    return readUser(
        name=name,
        email=credentials.email,
        profile_id=profile_id,
        profile_type=profile_type,
        token=token,
    )


@router.post("/update", response_model=readUser, status_code=status.HTTP_200_OK)
async def update_user(
    userData: Annotated[createUser, Body(...)],
    response: Response,
    user=Depends(user_metadata),
):

    # pull from db

    # see what changed
    # update based on it

    # return the new token
    return readUser(
        name=userData.name,
        email=userData.email,
        profile_id=user["profile_id"],  # profile id doesnt change
        profile_type=user["profile_type"],
        token=_issue_token(userData.name, user["profile_type"], user["profile_id"]),
    )


# since only a logged in user can delete their account
# the account information shall be identified from the token
@router.post("/delete", status_code=status.HTTP_200_OK, response_class=Response)
async def delete_user(response: Response, user=Depends(user_metadata)):

    # handle user deletion sequence
    logger.debug(f"""deleting user:
        [+] username {user}
    """)

    response.delete_cookie(
        "Bearer Token",
    )

    return Response(status_code=200, content={"message": "OK", "redirect": "/login"})
