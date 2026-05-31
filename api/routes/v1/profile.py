# Wagfu - Service Backend
# Profile fetch and manipulation endpoints
# updated: 26 Apr 2026

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from schemas.profile import (
    WriteDoctorProfile,
    WriteFacilitatorProfile,
    WritePetOwnerProfile,
    ReadDoctorProfile,
    ReadFacilitatorProfile,
    ReadPetOwnerProfile,
    UpdateDoctorProfile,
    UpdatePetOwnerProfile,
    UpdateFacilitatorProfile,
)

# configure export variables
__all__ = ["router"]

router = APIRouter(prefix="/profile")


@router.get(
    "/create",
    response_class=JSONResponse,
    response_model=(ReadDoctorProfile | ReadFacilitatorProfile | ReadPetOwnerProfile),
)
async def create_profile():
    pass
