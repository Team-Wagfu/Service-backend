# Wagfu - Service Backend
# Profile fetch and manipulation endpoints
# updated: 26 Apr 2026

from typing import Annotated
from fastapi import APIRouter, Depends, Body
from fastapi.responses import Response

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
from services.jwt.master import user_metadata

router = APIRouter(prefix="/profile")


@router.post(
    "/create",
    response_model=(ReadDoctorProfile | ReadFacilitatorProfile | ReadPetOwnerProfile),
)
async def create_profile(
    data: Annotated[
        WriteDoctorProfile | WriteFacilitatorProfile | WritePetOwnerProfile, Body(...)
    ],
    response: Response,
    userData=Depends(user_metadata),
):

    # read the profile id from the user_metadata
    # create the profile with the id
    # return the created profile

    # depending on the type of user identified from the token
    # the correponding models are sent as responses

    if isinstance(data, WriteDoctorProfile):
        # create the doctor profile and send the read model
        return ReadDoctorProfile()
    elif isinstance(data, WriteFacilitatorProfile):
        # create facilitator profile and send the read model
        return ReadFacilitatorProfile()
    elif isinstance(data, WritePetOwnerProfile):
        # create the petowner profile and send the read model
        return ReadPetOwnerProfile()


@router.post(
    "/update",
    response_model=(ReadDoctorProfile | ReadFacilitatorProfile | ReadPetOwnerProfile),
)
async def update_profile(
    data: Annotated[
        UpdatePetOwnerProfile | UpdateDoctorProfile | UpdateFacilitatorProfile,
        Body(...),
    ],
    response: Response,
    userData=Depends(user_metadata),
):

    if isinstance(data, WriteDoctorProfile):
        # update the model based on detected change and return corrected
        return ReadDoctorProfile()
    elif isinstance(data, WriteFacilitatorProfile):
        # update the model based on detected change and return corrected
        return ReadFacilitatorProfile()
    elif isinstance(data, WritePetOwnerProfile):
        # update the model based on detected change and return corrected
        return ReadPetOwnerProfile()


# configure export variables
__all__ = ["router"]
