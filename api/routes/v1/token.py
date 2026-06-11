"""
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.user import readUser
from services.jwt.master import user_metadata
from db.dependencies import get_db
from models.user import User
from core.exceptions import AuthenticationError

router = APIRouter(prefix="/token", tags=["token"])


@router.get("/token", response_model=readUser, status_code=status.HTTP_200_OK)
async def get_token(
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    profile_id = user.get("profile_id")
    stmt = select(User).where(User.profile_id == profile_id)
    db_user = session.scalar(stmt)
    if not db_user:
        raise AuthenticationError()

    return readUser(
        name=db_user.display_name,
        email=db_user.email,
        profile_id=db_user.profile_id,
    )

__all__ = ["router"]