# Wagfu Service Backend
# patient data retrieval and manipulation models
# Updated 28 Apr 2026

from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, TypedDict


# response models
# base configuration for all petient response classes
class PatientResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_to_lower=True,
        str_strip_whitespace=True,
        title="PatientResponse BaseClass",  # insignificant
    )

    count: Annotated[int, Field(default=0, description="number of patients")]
    status: Annotated[
        ResponseStatus,
        Field(default=ResponseStatus.error, description="status of the Response"),
    ]


# typed dict for patient data storage, representing a single patient
# given only the patient id(petid), the details of the pet can be retreived
class Patient(TypedDict):
    pet_name: Annotated[str, Field(...)]
    pet_id: Annotated[PetID, Field(...)]


class PatientList(PatientResponse):
    data: Annotated[
        list[Patient], Field(default_factory=[], description="list of pets")
    ]
