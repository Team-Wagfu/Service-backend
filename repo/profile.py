"""handle profile related crud operations"""

from uuid import uuid4
from datetime import date
from random import randint

from sqlalchemy import delete, select, text
from sqlalchemy.orm import Session
from models.profile import PetOwnerProfile, DoctorProfile, FacilitatorProfile
from schemas.profile import (
    WritePetOwnerProfile,
    WriteDoctorProfile,
    WriteFacilitatorProfile,
)
from schemas.profile import (
    ReadPetOwnerProfile,
    ReadDoctorProfile,
    ReadFacilitatorProfile,
)
from core.types import DocID, FacilitatorID, PetOwnerID

"""pydantic models are passed from which sqlmodels are constructed implicitely 
CRUD operation are conducted"""


class Profile:
    @staticmethod
    def createProfile(
        session: Session,
        profile_id: DocID | FacilitatorID | PetOwnerID,
        profile: WriteDoctorProfile | WriteFacilitatorProfile | WritePetOwnerProfile,
    ):
        # create uuid
        uuid = uuid4()
        user_id = f"-{date.today().year}-" + str(randint(1, 10000)).zfill(
            5
        )  # corresponds to id

        if isinstance(profile, WriteDoctorProfile):
            # create id for doctor profile
            # assuming random for now

            user_id = "DOC" + user_id
            to_write = WriteDoctorProfile(id=user_id, **profile)

        elif isinstance(profile, WritePetOwnerProfile):
            # create id for pet owner profile
            user_id = "OWN" + user_id
            to_write = WritePetOwnerProfile(id=user_id, **profile)

        elif isinstance(profile, WriteFacilitatorProfile):
            # create id from facilitator profile
            user_id = "FAC" + user_id
            to_write = WriteFacilitatorProfile(id=user_id, **profile)

        session.add(to_write)
        session.flush()

        session.refresh(to_write)

        return to_write

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
        elif profile_id.startswith("FAC") or profile_id.startswith("CLN") or profile_id.startswith("PHM"):
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


__all__ = ["Profile"]
