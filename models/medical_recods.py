# Wagfu Service Backend
# medical records table and related schemas
# Updated 1 May 2026

from sqlmodel import SQLModel, Field
from typing import Annotated
from app.core.types import MedicalRecordID, PetID

class MedicalRecord(SQLModel, table=True):
    
    med_report_id: Annotated[MedicalRecordID, Field(..., primary_key=True, description="medical report id")]
    pet_id: Annotated[PetID, Field(..., description="pet report id")]
    filename: Annotated[str, Field(..., description="filename hashedd from med_report_id and pet_id")]
