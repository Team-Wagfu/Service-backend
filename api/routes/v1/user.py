"""
router handling user creation sequence
"""

from fastapi import APIRouter, Body
from typing import Annotated
from schemas.user import User

router = APIRouter(prefix="/user", tags=["user", "registration"])


@router.post("/create")
async def create_user(userData: Annotated[User, Body(...)]):
    pass
