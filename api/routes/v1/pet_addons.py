"""
Vaccination and medical record routes wired to pets and doctors.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from db.dependencies import get_db
from schemas.pet_addons import (
    createMedicalRecord,
    createVaccination,
    readMedicalRecord,
    readVaccination,
    updateMedicalRecord,
    updateVaccination,
)
from services.jwt.master import user_metadata
from services.pet_addons import PetAddonService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("Starting pet addon routes")
router = APIRouter(
    prefix="/pet",
    tags=["pet", "vaccination", "medical-records"],
)


@router.post(
    "/vaccination/create",
    response_model=readVaccination,
    status_code=status.HTTP_201_CREATED,
)
async def create_vaccination(
    payload: Annotated[createVaccination, Body(...)],
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetAddonService.create_vaccination(
        payload,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.get(
    "/vaccination/list/{pet_id}",
    response_model=list[readVaccination],
    status_code=status.HTTP_200_OK,
)
async def list_vaccinations(
    pet_id: str,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetAddonService.list_vaccinations(
        pet_id,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.post(
    "/vaccination/update",
    response_model=readVaccination,
    status_code=status.HTTP_200_OK,
)
async def update_vaccination(
    payload: Annotated[updateVaccination, Body(...)],
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetAddonService.update_vaccination(
        payload,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.post(
    "/medical/create",
    response_model=readMedicalRecord,
    status_code=status.HTTP_201_CREATED,
)
async def create_medical_record(
    payload: Annotated[createMedicalRecord, Body(...)],
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetAddonService.create_medical_record(
        payload,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.get(
    "/medical/list/{pet_id}",
    response_model=list[readMedicalRecord],
    status_code=status.HTTP_200_OK,
)
async def list_medical_records_for_pet(
    pet_id: str,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetAddonService.list_medical_records_for_pet(
        pet_id,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.get(
    "/medical/doctor/list",
    response_model=list[readMedicalRecord],
    status_code=status.HTTP_200_OK,
)
async def list_medical_records_for_doctor(
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetAddonService.list_medical_records_for_doctor(
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )


@router.post(
    "/medical/update",
    response_model=readMedicalRecord,
    status_code=status.HTTP_200_OK,
)
async def update_medical_record(
    payload: Annotated[updateMedicalRecord, Body(...)],
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return PetAddonService.update_medical_record(
        payload,
        user.get("profile_id", ""),
        user.get("role", ""),
        session,
    )
