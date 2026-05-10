# Wagfu Service Backend
# pet related db models
# Updated 8 May 2026

from datetime import date, datetime

from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy import Date, Boolean

from models.base import Base
from models.types import UpString, LowString, UInteger
from models.enums import Animals


class Pets(Base):
    """pet data"""

    __tablename__ = "pets"

    pet_id = Column(
        UpString(15),  # enforece strict size, PET-0000-00000,
        primary_key=True,
    )

    # id, from user, slug formatted
    owner_id = Column(
        UpString(15),
        ForeignKey("pet_owner_profile.id"),
        nullable=False,
        primary_key=True,
    )

    name = Column(
        LowString,
        nullable=False,
    )

    type = Column(
        Enum(Animals, name="animals_enum"),
        nullable=False,
    )

    breed = Column(
        LowString,
        nullable=False,
    )

    color = Column(LowString, nullable=False)

    weight = Column(UInteger, nullable=False)

    height = Column(UInteger, nullable=False)

    owner = relationship("PetOwnerProfile", back_populates="pet")
    vaccination = relationship(
        "Vaccination", back_populates="pet", cascade="all, delete-orphan"
    )
    medical_records = relationship(
        "MedicalRecords", back_populates="pet", cascade="all, delete-orphan"
    )


class Vaccination(Base):
    """vaccination details of pets"""

    __tablename__ = "vaccinations"

    # id of the pet to whic hteh record belongs to
    pet_id = Column(UpString, ForeignKey("pets.pet_id"))

    # name of the vaccination
    vaccine = Column(LowString, nullable=False)

    # date by which the vaccination should be taken
    due_date = Column(Date, nullable=False)

    # whether the vaccination was completed or not
    # not nullable, its either true or false
    status = Column(Boolean, default=False, nullable=False)

    # vaccinated at, the clinic id, identifying clinic
    # null in case of vaccination not acquired yet
    vaccinated_at = Column(
        LowString, ForeignKey("clinic.id"), nullable=True
    )  # Facility name

    # vaccinated by, identified by doctor id
    # null in case of not acquired yet
    vaccinated_by = Column(LowString, ForeignKey("doctor_profile.id"), nullable=True)

    # date at which the vaccination was done
    # can be null in case of not acquired yet
    vaccinated_on = Column(Date, nullable=True)

    # id of the medical report for getting detailed insdight
    # into further details of the medication
    report = Column(UpString)  # Medical report ID

    pet = relationship("pets", back_populates="vaccination")


class MedicalRecords(Base):
    """medical record mapping table, records parsed and returned using ETL system"""

    __tablename__ = "medical_records"

    # unique identifier
    medical_id = Column(
        UpString(15),
        primary_key=True,
        nullable=False,
    )

    # id of the pet to which the medical record is concerned to
    pet_id = Column(
        UpString(15),
        nullable=False,
    )

    # corresponding doctor who handled the medication
    doctor_id = Column(
        UpString,
        ForeignKey("doctor_profile.id"),
        nullable=False,
    )

    diagnosis = Column(LowString, nullable=False, default="")

    date = Column(Date, nullable=False, default=date.today)

    pet = relationship("Pets", back_populates="medical_records")
