"""handle profile related crud operations"""

from uuid import uuid4
from datetime import date
from random import randint

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

"""pydantic models are passed from which sqlmodels are constructed implicitely 
CRUD operation are conducted"""


class Profile:  # TODO
    @staticmethod
    def createProfile(
        db: Session,
        profile: WriteDoctorProfile | WriteFacilitatorProfile | WritePetOwnerProfile,
    ):
        # create uuid
        uuid = uuid4()

        if isinstance(profile, WriteDoctorProfile):
            # create id for doctor profile
            # assuming random for now
            user_id = f"DOC-{date.today().year}-" + str(randint(1, 10000)).zfill(5)

        elif isinstance(profile, WritePetOwnerProfile):
            # create id for pet owner profile
            pass
        elif isinstance(profile, WriteFacilitatorProfile):
            # create id from facilitator profile
            pass

        #
