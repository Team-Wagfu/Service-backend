# Wagfu Service Backend
# vaccination and medical record request/response models
# Updated 10 Jun 2026

from datetime import date
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field

from core.types import PetID, DocID, MedicalRecordID, ClinicID


class createVaccination(BaseModel):
    """schedule a vaccination for a pet"""

    pet_id: PetID
    vaccine: Annotated[str, Field(..., min_length=1, max_length=50)]
    due_date: Annotated[date, Field(...)]

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class readVaccination(BaseModel):
    pet_id: PetID
    vaccine: str
    due_date: date
    status: bool
    vaccinated_at: Annotated[
        Optional[ClinicID], Field(default=None, description="facility id")
    ]
    vaccinated_by: Annotated[
        Optional[DocID], Field(default=None, description="administering doctor id")
    ]
    vaccinated_on: Optional[date] = None
    report: Annotated[
        Optional[MedicalRecordID],
        Field(default=None, description="linked medical record id"),
    ]

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)


class updateVaccination(BaseModel):
    pet_id: PetID
    vaccine: Annotated[str, Field(..., min_length=1, max_length=50)]
    due_date: Optional[date] = None
    status: Optional[bool] = None
    vaccinated_at: Optional[ClinicID] = None
    vaccinated_on: Optional[date] = None
    report: Optional[MedicalRecordID] = None

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class createMedicalRecord(BaseModel):
    """doctor-authored diagnosis entry for a pet"""

    pet_id: PetID
    diagnosis: Annotated[str, Field(..., min_length=1, max_length=500)]
    record_date: Annotated[
        date, Field(default_factory=date.today, alias="date")
    ]

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        populate_by_name=True,
    )


class readMedicalRecord(BaseModel):
    medical_id: MedicalRecordID
    pet_id: PetID
    doctor_id: DocID
    diagnosis: str
    record_date: Annotated[date, Field(alias="date")]

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True, populate_by_name=True)


class updateMedicalRecord(BaseModel):
    medical_id: MedicalRecordID
    diagnosis: Optional[Annotated[str, Field(min_length=1, max_length=500)]] = None
    record_date: Annotated[Optional[date], Field(default=None, alias="date")] = None

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        populate_by_name=True,
    )
