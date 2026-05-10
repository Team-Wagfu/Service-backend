"""
Wagfu service backend
models for user profile extension
Updated 8 May 2026
"""

from decimal import Decimal

from sqlalchemy import Column, CheckConstraint, and_, ForeignKey
from sqlalchemy import String, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import validates, relationship

from models.base import Base

from models.user import User  # noqa: F401
from models.types import UpString, LowString, UInteger
from core.types import IdTypeAdapter as a


class PetOwnerProfile(Base):
    """pet owner profile"""

    __tablename__ = "pet_owner_profile"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
    )

    # generalised column name `id` for program specific user id
    # of each type of user
    id = Column(
        UpString(15),
        primary_key=True,
        nullable=False,
    )

    # check if the id format is valid
    @validates("id")
    def validate_pet_owner_id(self, key, value) -> str:
        """id follows required format"""

        a.petowner.validate_python(value)
        return value

    # approximate location of the user, mutability to avoid dirty orm
    location = Column(
        MutableDict.as_mutable(
            JSONB(
                none_as_null=True,
            )
        ),
        nullable=False,
        default=lambda: {},  # need to enale automatic location detection and populate it with current location
    )

    # the location json should contain the keys lat and lng
    @validates("location")
    def validate_location(self, key, value) -> JSONB:
        """location has lat and lng keys and values of appropriate type"""

        if "lat" not in value:
            raise KeyError("missing key, lat")
        elif "lng" not in value:
            raise KeyError("missing key, lng")
        elif not isinstance(value["lat"], float) or not isinstance(value["lng"], float):
            raise ValueError("Invalid type for coordinates")
        return value

    # TODO
    # make sure the values being appended into the list are ids
    # that exists in the pet table
    pet_ids = Column(
        MutableDict.as_mutable(ARRAY(String)),
        nullable=False,
        default=list,
    )

    user = relationship("User", back_populates="pet_owner_profile", use_list=False)
    pet = relationship("Pets", back_populates="owner")


# doctor profile,
# unverified, HOW TO ????????
class DoctorProfile(Base):
    """doctor profile including doctor metadata"""

    __tablename__ = "doctor_profile"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
    )

    id = Column(
        UpString(15),
        primary_key=True,
        nullable=False,
    )

    # particular specialization of the doctor, if any
    specialization = Column(LowString, nullable=False, default="general")

    # number of years of experience
    experience = Column(UInteger, nullable=False, default=0)

    # rating is intitially emppty(0)
    rating = Column(Numeric(2, 2), nullable=False, default=Decimal("0.00"))

    # number of ratings
    rating_count = Column(UInteger, nullable=False, default=0)

    user = relationship("User", back_populates="doctor_profile")
    clinics = relationship("Clinic", back_populates="doctor")

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

    user = relationship("User", back_populates="doctor_profile", use_list=False)


class AdminProfile(Base):
    """admin profile table"""

    __tablename__ = "admin"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)

    id = Column(UpString(15), nullable=False, primary_key=True)

    user = relationship("User", back_populates="admin_profile")


__all__ = ["PetOwnerProfile", "AdminProfile", "DoctorProfile"]
