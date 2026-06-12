# Wagfu - Service Backend
# Profile fetch and manipulation endpoints
# updated: 26 Apr 2026

from typing import Annotated, Union
from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

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
from db.dependencies import get_db
from models.user import User
from models.profile import PetOwnerProfile, DoctorProfile, FacilitatorProfile
from core.exceptions import AuthenticationError, AppError
from core.types import Address

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@router.post(
    "/create",
    response_model=Union[ReadDoctorProfile, ReadFacilitatorProfile, ReadPetOwnerProfile],
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    data: Annotated[
        WriteDoctorProfile | WriteFacilitatorProfile | WritePetOwnerProfile, Body(...)
    ],
    userData=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    profile_id = userData.get("profile_id")
    if not profile_id:
        raise AuthenticationError()

    # Fetch the user to get the user_id (UUID)
    stmt = select(User).where(User.profile_id == profile_id)
    db_user = session.scalar(stmt)
    if not db_user:
        raise AuthenticationError()

    # Determine which profile to create/update
    if isinstance(data, WriteDoctorProfile):
        stmt = select(DoctorProfile).where(DoctorProfile.id == profile_id)
        profile = session.scalar(stmt)
        if not profile:
            profile = DoctorProfile(
                id=profile_id,
                user_id=db_user.user_id,
                specialization=data.specialisation,
                experience=data.experience,
            )
            session.add(profile)
        else:
            profile.specialization = data.specialisation
            profile.experience = data.experience
        
        try:
            session.commit()
            session.refresh(profile)
        except Exception as e:
            session.rollback()
            raise AppError(msg="Failed to create/update profile", status_code=500)
            
        # Return default address as DoctorProfile does not store it in DB
        return ReadDoctorProfile(
            id=profile.id,
            address=Address(),
            specialisation=profile.specialization,
            experience=profile.experience,
            rating=int(profile.rating),
            rating_count=profile.rating_count
        )

    elif isinstance(data, WriteFacilitatorProfile):
        stmt = select(FacilitatorProfile).where(FacilitatorProfile.id == profile_id)
        profile = session.scalar(stmt)
        if not profile:
            profile = FacilitatorProfile(
                id=profile_id,
                user_id=db_user.user_id,
                name=data.name,
                description=data.description,
                address=data.address.model_dump(),
                type=data.type,
                links=data.links.model_dump() if hasattr(data.links, "model_dump") else data.links
            )
            session.add(profile)
        else:
            profile.name = data.name
            profile.description = data.description
            profile.address = data.address.model_dump()
            profile.type = data.type
            profile.links = data.links.model_dump() if hasattr(data.links, "model_dump") else data.links
            
        try:
            session.commit()
            session.refresh(profile)
        except Exception as e:
            session.rollback()
            raise AppError(msg="Failed to create/update profile", status_code=500)
            
        return ReadFacilitatorProfile(
            id=profile.id,
            address=profile.address,
            name=profile.name,
            description=profile.description,
            links=profile.links
        )

    elif isinstance(data, WritePetOwnerProfile):
        stmt = select(PetOwnerProfile).where(PetOwnerProfile.id == profile_id)
        profile = session.scalar(stmt)
        if not profile:
            profile = PetOwnerProfile(
                id=profile_id,
                user_id=db_user.user_id,
                location=data.location,
                address=data.address.model_dump(),
                pet_ids=data.pet_ids
            )
            session.add(profile)
        else:
            profile.location = data.location
            profile.address = data.address.model_dump()
            profile.pet_ids = data.pet_ids
            
        try:
            session.commit()
            session.refresh(profile)
        except Exception as e:
            session.rollback()
            raise AppError(msg="Failed to create/update profile", status_code=500)
            
        return ReadPetOwnerProfile(
            id=profile.id,
            address=profile.address,
            pet_ids=profile.pet_ids
        )


@router.post(
    "/update",
    response_model=Union[ReadDoctorProfile, ReadFacilitatorProfile, ReadPetOwnerProfile],
)
async def update_profile(
    data: Annotated[
        UpdatePetOwnerProfile | UpdateDoctorProfile | UpdateFacilitatorProfile,
        Body(...),
    ],
    userData=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    profile_id = userData.get("profile_id")
    if not profile_id:
        raise AuthenticationError()

    if isinstance(data, UpdateDoctorProfile):
        stmt = select(DoctorProfile).where(DoctorProfile.id == profile_id)
        profile = session.scalar(stmt)
        if not profile:
            raise AuthenticationError()
        
        if data.specialisation is not None:
            profile.specialization = data.specialisation
        if data.experience is not None:
            profile.experience = data.experience
        
        try:
            session.commit()
            session.refresh(profile)
        except Exception as e:
            session.rollback()
            raise AppError(msg="Failed to update profile", status_code=500)
            
        return ReadDoctorProfile(
            id=profile.id,
            address=Address(),
            specialisation=profile.specialization,
            experience=profile.experience,
            rating=int(profile.rating),
            rating_count=profile.rating_count
        )

    elif isinstance(data, UpdateFacilitatorProfile):
        stmt = select(FacilitatorProfile).where(FacilitatorProfile.id == profile_id)
        profile = session.scalar(stmt)
        if not profile:
            raise AuthenticationError()
        
        if data.name is not None:
            profile.name = data.name
        if data.description is not None:
            profile.description = data.description
        if data.address is not None:
            profile.address = data.address.model_dump()
        if data.type is not None:
            profile.type = data.type
        if data.links is not None:
            profile.links = data.links.model_dump()
            
        try:
            session.commit()
            session.refresh(profile)
        except Exception as e:
            session.rollback()
            raise AppError(msg="Failed to update profile", status_code=500)
            
        return ReadFacilitatorProfile(
            id=profile.id,
            address=profile.address,
            name=profile.name,
            description=profile.description,
            links=profile.links
        )

    elif isinstance(data, UpdatePetOwnerProfile):
        stmt = select(PetOwnerProfile).where(PetOwnerProfile.id == profile_id)
        profile = session.scalar(stmt)
        if not profile:
            raise AuthenticationError()
        
        if data.address is not None:
            profile.address = data.address.model_dump()
        if data.pet_ids is not None:
            profile.pet_ids = data.pet_ids
            
        try:
            session.commit()
            session.refresh(profile)
        except Exception as e:
            session.rollback()
            raise AppError(msg="Failed to update profile", status_code=500)
            
        return ReadPetOwnerProfile(
            id=profile.id,
            address=profile.address,
            pet_ids=profile.pet_ids
        )


# delete operations are handled implicitely when the user account is deleted

# configure export variables
__all__ = ["router"]
