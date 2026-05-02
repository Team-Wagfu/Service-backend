# Wagfu Service Backend
# pet related db models
# Updated 28 Apr 2026

from sqlmodel import SQLModel, Field

from typing import Annotated
from datetime import date
from app.models.types import PetID, PetOwnerID, MedicalRecordID
from app.models.enums import *


# general information of pet identified by respective PetID
class Pets(SQLModel, table=True):
    pet_id: Annotated[PetID, Field(None, primary_key=True, index=True)] # improve
    name: Annotated[str, Field(..., max_length=50, min_length=3, description="name of the pet")]
    dob: Annotated[date, Field(..., description="date of birth of pet")]
    type: Annotated[Animals, Field(..., description="type of pet from the type enum")]
    breed: Annotated[str, Field(..., description="breed of the pet")]
    color: Annotated[str, Field(..., description="color of the pet")]
    weight: Annotated[float, Field(..., gt=0, description="weight of pet in KG")]
    height: Annotated[float, Field(..., gt=0, description="height of pet in CM")]

# vaccination information
class Vaccination(SQLModel, table=True):
    pet_id: Annotated[PetID, Field(None, primary_key=True, index=True)]
    vaccine: Annotated[str, Field(..., primary_key=True, index=True)]
    due_date: Annotated[date, Field(..., description="date before which the vaccine should be taken")]
    status: Annotated[bool, Field(default=0, description="status, whether the vaccination was completed or not")]
    vaccinated_at: Annotated[str, ]
