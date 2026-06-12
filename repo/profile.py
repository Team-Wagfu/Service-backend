"""handle profile related crud operations"""

from uuid import uuid4, UUID
from datetime import date
from random import randint

from sqlalchemy import delete, select, text
from sqlalchemy.orm import Session
from models.profile import PetOwnerProfile, DoctorProfile, FacilitatorProfile
from core.enums import UserType
from schemas.profile import (
    WritePetOwnerProfile,
    WriteDoctorProfile,
    WriteFacilitatorProfile,
)
from core.types import DocID, FacilitatorID, PetOwnerID

"""pydantic models are passed from which sqlmodels are constructed implicitely 
CRUD operation are conducted"""


class Profile:
    @staticmethod
    def create_default_profile(
        session: Session,
        user_id: UUID,
        id: DocID | FacilitatorID | PetOwnerID,
        user_type: UserType,
    ):
        """Create a profile with default values upon user registration."""
        print(f"DEBUG: create_default_profile called for {user_id}, {id}, {user_type}")
        default_location = {"lat": 0.0, "lng": 0.0}
        default_address = {
            "address_line_1": "unknown",
            "street": "unknown",
            "locality": "unknown",
            "city": "unknown",
            "district": "unknown",
            "state": "unknown",
            "postal_code": 1,
        }

        if user_type == UserType.doctor:
            profile = DoctorProfile(
                id=id,
                user_id=user_id,
                specialization="General",
                experience=0,
            )
        elif user_type == UserType.owner:
            profile = PetOwnerProfile(
                id=id,
                user_id=user_id,
                location=default_location,
                address=default_address,
                pet_ids=[],
            )
        elif user_type == UserType.facilitator:
            profile = FacilitatorProfile(
                id=id,
                user_id=user_id,
                address=default_address,
                name="New Facility",
                description="Default description",
                type="pharmaceutical",
                links={},
            )
        else:
            return None

        session.add(profile)
        session.flush()
        return profile

    @staticmethod
    def createProfile(
        session: Session,
        profile_id: DocID | FacilitatorID | PetOwnerID,
        profile: WriteDoctorProfile | WriteFacilitatorProfile | WritePetOwnerProfile,
    ):
        # Implementation moved to routes or handled here. 
        # This old method is inconsistent.
        pass

    # change from hard delete to soft delete
    @staticmethod
    def delete_profile(
        session: Session,
        profile_id: FacilitatorID | PetOwnerID | DocID,
    ):
        """delete the corresponding profile"""
        _ = None
        if profile_id.startswith("DOC"):
            _ = DoctorProfile
        elif (
            profile_id.startswith("FAC")
            or profile_id.startswith("CLN")
            or profile_id.startswith("PHM")
        ):
            _ = FacilitatorProfile
        elif profile_id.startswith("OWN") or profile_id.startswith("PW"):
            _ = PetOwnerProfile

        if _:
            stmt = delete(_).where(_.id == profile_id)
            session.execute(stmt)

    @staticmethod
    def update_profile(
        session: Session,
        profile_id: FacilitatorID | PetOwnerID | DocID,
        data: FacilitatorProfile | PetOwnerProfile | DoctorProfile,
    ):
        """handle profile updates"""
        pass


__all__ = ["Profile"]
