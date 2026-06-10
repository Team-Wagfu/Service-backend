"""
Pet registration and management endpoints.

Pets are created under the authenticated pet owner's profile and linked
via the owner's pet_ids array.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from db.dependencies import get_db
from schemas.pets import createPet, readPet, updatePet
from services.jwt.master import user_metadata
from services.pet import PetService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("Starting /pet router")
router = APIRouter(
    prefix="/pet",
    tags=["pet"],
)


@router.post("/create", response_model=readPet, status_code=status.HTTP_201_CREATED)
async def create_pet(
    petData: Annotated[createPet, Body(...)],
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    logger.debug(
        """creating pet:
        [+] name    %s
        [+] type    %s
        [+] owner   %s
    """,
        petData.name,
        petData.type,
        user.get("profile_id"),
    )

    return PetService.create(
        petData,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.get("/list", response_model=list[readPet], status_code=status.HTTP_200_OK)
async def list_pets(
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetService.list_by_owner(
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.get("/{pet_id}", response_model=readPet, status_code=status.HTTP_200_OK)
async def get_pet(
    pet_id: str,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetService.get(
        pet_id,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.post("/update", response_model=readPet, status_code=status.HTTP_200_OK)
async def update_pet(
    petData: Annotated[updatePet, Body(...)],
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetService.update(
        petData,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.delete("/delete/{pet_id}", status_code=status.HTTP_200_OK, response_class=Response)
async def delete_pet(
    pet_id: str,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    PetService.delete(
        pet_id,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )

    return Response(status_code=200, content={"message": "OK"})
