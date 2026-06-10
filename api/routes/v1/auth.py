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

from schemas.user import createUser, readUser
from services.jwt.master import user_metadata
from services.jwt.helper import create_jwt
from db.dependencies import get_db

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

    # token creation and profile_id grepping

    profile_type: str = userData.type
    profile_id: str = ""  # profile id here

    now = datetime.now(timezone.utc)

    token: str = create_jwt(
        {
            "name": userData.name,
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
    return readUser(name=userData.name, email=userData.email, profile_id=profile_id)


@router.post("/update", response_model=readUser, status_code=status.HTTP_200_OK)
async def update_user(
    userData: Annotated[createUser, Body(...)],
    response: Response,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):

    # see what changed
    # update based on it

    # return the new token
    return readUser(
        name=userData.name,
        email=userData.email,
        profile_id=user.profile_id,  # profile id doesnt change
    )


# since only a logged in user can delete their account
# the account information shall be identified from the token
@router.delete("/delete", status_code=status.HTTP_200_OK, response_class=Response)
async def delete_user(
    response: Response,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):

    # handle user deletion sequence

    # remove token
    # send redirect to /login
    # delet profile
    # delete user

    logger.debug(
        """deleting user:
        [+] username %s""",
        user,
    )

    response.delete_cookie(
        "Bearer",
    )

    return Response(status_code=200, content={"message": "OK", "redirect": "/login"})


# logout
@router.post("/logout", status_code=status.HTTP_200_OK, response_class=Response)
async def logout_user(response: Response, user=Depends(user_metadata)):

    # handle logout sequence
    return Response(status_code=200, content={"message": "OK", "redirect": "/login"})
