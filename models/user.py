"""
Wagfu service backend
user models
Updated 8 May 2026
"""

import uuid
from datetime import date, datetime, UTC
from sqlalchemy import Column, Enum
from sqlalchemy import Boolean, Date, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.types import CapString, LowString
from models.enums import UserType
from models.base import Base


class User(Base):
    """user model"""

    __tablename__ = "users"

    # a uuid identifying every user irrespective of the type and profile
    user_id = Column(
        UUID(
            as_uuid=True
        ),  # uuid type, parsed as uuid.uuid4 python object rather than string
        primary_key=True,
        default=uuid.uuid4,
    )

    # the type of the user, with which the corresponsing role in the db and profile
    # are matched and populated
    type = Column(
        Enum(UserType, name="enum_usertype"),  # define a sql enum, and use it
        nullable=False,
        default=UserType.PET_OWNER,
    )

    # a simple display name to identify the user and show as username in the application
    display_name = Column(CapString(50), nullable=False)

    # email of the user
    email = Column(LowString, nullable=False)

    # column consisting of the unique id of user, slug included one
    # to identify the user profile in particular profile table
    #
    # nullable=True,
    # when the user registers, the identity exists only in the Users
    # hence, only after creating a corresponding profile, the user
    # profile can be linked, hence the nullability
    profile_id = Column(String(15), nullable=True, unique=True)

    # date at which the account was created
    created_at = Column(Date, nullable=False, default=date.today)

    # last login date will be same as the day of account creation
    # by default, any subsequent logins will be recorded next
    last_login = Column(Date, nullable=False, default=date.today)

    # every time the column is updated through orm, the column value is updated accodingly
    # and no server updates change the value, only orm interactions
    updated_on = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(
            UTC
        ),  # updated through orm will only invoke this, SERVER UPDATES ARE UN-MONITORED
    )

    # the account is marked as active by default and upon deletion(deactivation),
    # it is marked as False,
    # and after the restoration period, the record is removed cascadingly
    active = Column(Boolean, nullable=False, default=True)

    # relationships
    pet_owner_profile = relationship(
        "PetOwnerProfile",
        back_populates="user",
        uselist=False,
    )
    doctor_profile = relationship(
        "DoctorProfile",
        back_populates="user",
        uselist=False,
    )
    admin_profile = relationship(
        "AdminProfile",
        back_populates="user",
        uselist=False,
    )
    clinic_profile = relationship(
        "ClinicProfile",
        back_populates="user",
        uselist=False,
    )

    # emergency_profile = relationship(
    #     "EmergencyProfile",
    #     back_populates="user",
    #     uselist=False,
    # )
    # pharmacy_profile = relationship(
    #     "PharmaceuticalProfile",
    #     back_populates="user",
    #     uselist=False,
    # )


__all__ = ["User"]
