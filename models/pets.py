# Wagfu Service Backend
# pet related db models
# Updated 8 May 2026

from datetime import date

from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, Enum, ForeignKey, PrimaryKeyConstraint
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

    pet_id = Column(
        UpString(15),
        ForeignKey("pets.pet_id"),
        nullable=False,
        index=True,
    )

    vaccine = Column(LowString, nullable=False)

    # date by which the vaccination should be taken
    due_date = Column(Date, nullable=False)

    # whether the vaccination was completed or not
    # not nullable, its either true or false
    status = Column(Boolean, default=False, nullable=False)

    # clinic or facility id; nullable until vaccination is administered
    vaccinated_at = Column(LowString, nullable=True)

    # vaccinated by, identified by doctor id
    # null in case of not acquired yet
    vaccinated_by = Column(LowString, ForeignKey("doctor_profile.id"), nullable=True)

    # date at which the vaccination was done
    # can be null in case of not acquired yet
    vaccinated_on = Column(Date, nullable=True)

    # id of the medical report for getting detailed insdight
    # into further details of the medication
    report = Column(UpString)

    pet = relationship("Pets", back_populates="vaccination")
    doctor = relationship(
        "DoctorProfile",
        foreign_keys=[vaccinated_by],
        primaryjoin="Vaccination.vaccinated_by == DoctorProfile.id",
    )

    __table_args__ = (PrimaryKeyConstraint("pet_id", "vaccine"),)


class MedicalRecords(Base):
    """medical record mapping table, records parsed and returned using ETL system"""

    __tablename__ = "medical_records"

    # unique identifier
    medical_id = Column(
        UpString(15),
        primary_key=True,
        nullable=False,
    )

    pet_id = Column(
        UpString(15),
        ForeignKey("pets.pet_id"),
        nullable=False,
        index=True,
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
    doctor = relationship(
        "DoctorProfile",
        foreign_keys=[doctor_id],
        primaryjoin="MedicalRecords.doctor_id == DoctorProfile.id",
    )
