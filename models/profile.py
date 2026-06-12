"""
Wagfu service backend
models for user profile extension
Updated 8 May 2026
"""

from decimal import Decimal

from sqlalchemy import Column, CheckConstraint, and_, ForeignKey
from sqlalchemy import String, Numeric
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import validates, relationship

from models.base import Base
from models.enums import FacilityTypeEnum

from models.types import (
    UpString,
    LowString,
    UInteger,
    SocialsJSONB,
    CoordinateJSONB,
    AddressJSONB,
)
from core.types import IdTypeAdapter as a


class PetOwnerProfile(Base):
    """pet owner profile"""

    __tablename__ = "pet_owner_profile"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        # primary_key=True,
    )

    # generalised column name `id` for program specific user id
    # of each type of user
    id = Column(
        UpString(15),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )

    # check if the id format is valid
    @validates("id")
    def validate_pet_owner_id(self, key, value) -> str:
        """id follows required format"""

        a.petowner.validate_python(value)
        return value

    # approximate location of the user, mutability to avoid dirty orm
    location = Column(
        CoordinateJSONB,
        default={},  # need to enale automatic location detection and populate it with current location
    )

    # insertion and retrieval takes the model core.types.Address
    # when inserting, use Address.model_dump() to retrieve the dict and pass to insertion function
    address = Column(AddressJSONB, default={})

    # make sure the values being appended into the list are ids
    # that exists in the pet table
    pet_ids = Column(
        MutableList.as_mutable(ARRAY(String)),
        nullable=False,
        default=list,
    )

    user = relationship("User", back_populates="pet_owner_profile", uselist=False)
    pet = relationship("Pets", back_populates="owner")


# doctor profile,
# unverified, HOW TO ????????
class DoctorProfile(Base):
    """doctor profile including doctor metadata"""

    __tablename__ = "doctor_profile"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        # primary_key=True,
    )

    id = Column(
        UpString(15),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )

    # particular specialization of the doctor, if any
    specialization = Column(LowString(50), nullable=False, default="general")

    # number of years of experience
    experience = Column(UInteger, nullable=False, default=0)

    # rating is intitially emppty(0)
    rating = Column(Numeric(2, 2), nullable=False, default=Decimal("0.00"))

    # number of ratings
    rating_count = Column(UInteger, nullable=False, default=0)

    user = relationship("User", back_populates="doctor_profile")
    # clinics = relationship("ClinicProfile", back_populates="doctor")

    __table_args__ = (
        CheckConstraint(and_(experience >= 0), name="ck_experience_duration"),
        CheckConstraint(
            and_(
                rating >= 0.0,
                rating <= 10.0,
            ),
            name="ck_rating_range",
        ),
    )

    user = relationship("User", back_populates="doctor_profile", uselist=False)


class AdminProfile(Base):
    """admin profile table"""

    __tablename__ = "admin_profile"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)

    id = Column(UpString(15), nullable=False, primary_key=True)

    user = relationship("User", back_populates="admin_profile")


class FacilitatorProfile(Base):
    """facilitator profile table"""

    __tablename__ = "facilitator_profile"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        # primary_key=True,
        index=True,
    )

    id = Column(
        UpString(15),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )

    # name of the facility
    name = Column(LowString(100), nullable=False)

    # a  short description about the website
    # can be markdown formatted if specified
    description = Column(LowString(150), nullable=False, default="")

    # address of the facilitator
    address = Column(AddressJSONB, nullable=False, default={})

    # facility type
    type = Column(
        FacilityTypeEnum,
        nullable=False,
    )

    # wesbite or other links
    links = Column(
        SocialsJSONB,
    )

    user = relationship("User", back_populates="clinic_profile", uselist=False)


__all__ = ["PetOwnerProfile", "AdminProfile", "DoctorProfile", "FacilitatorProfile"]
