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
from datetime import datetime, timedelta

from schemas.user import createUser, readUser
from services.jwt.master import user_metadata
from services.jwt.helper import create_jwt

logger = logging.getLogger(__name__)

logger.info("Starting /user router")
router = APIRouter(prefix="/user", tags=["user", "registration"])


@router.post("/create", response_model=readUser, status_code=status.HTTP_201_CREATED)
async def create_user(userData: Annotated[createUser, Body(...)], response: Response):

    # handle user creation
    logger.debug(f"""creating user:
        [+] username    {userData.name}
        [+] email       {userData.email}
        [*] passwd      {userData.pwd}
    """)

    # token creation and profile_id grepping

    profile_id: str = ""  # profile id here

    token: str = create_jwt(
        {
            "name": userData.name,
            "expiry": datetime.now() + timedelta(days=7),  # 7 day window
            "profile_id": profile_id,
        }
    )
    logger.debug(f"creating token {token}")

    logger.debug(f"""data:
        [+] token       {token}
        [+] profile_id  {profile_id}
    """)

    response.set_cookie(key="Bearer Token", value=token, httponly=True)

    return readUser(name=userData.name, email=userData.email, profile_id=profile_id)


# since only a logged in user can delete their account
# the account information shall be identified from the token
@router.post("/delete", status_code=status.HTTP_200_OK, response_class=Response)
async def delete_user(response: Response, user=Depends(user_metadata)):

    # handle user deletion sequence
    logger.debug(f"""deleting user:
        [+] username {user}
    """)
