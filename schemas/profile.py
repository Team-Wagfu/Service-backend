# Wagfu service backend
# profile schemas for defining request response pydantic models
# Updated 26 Apr 2026

from pydantic import Annotated, Field, BaseModel, ConfigDict
from Enum import enum

# response models

# Response model for profile request, requested with the corresponding user id
# user if format DOC-2026-00001
class DoctorResponse(BaseModel):
    model_config=ConfigDict(   
        extra="forbid",
        str_to_lower=True,
        str_strip_whitespace=True,
        str_min_length=3,
        title="DoctorResponse BaseClass" # insignificant
    )


# profile query response model
class DoctorProfileResponse(DoctorResponse):
    name: Annotated[str, Field(..., description="name of the doctor")]
    # TODO, need to implement as precise list of available qualification
    qual: Annotated[str, Field(..., description="highest qualification of the doc")]
    spec: Annotated[str, Field(..., description="particular specialisation of the doc")]
    exp: Annotated[int, Field(default=0, description="number of years of verfied experience")]
    # TODO, privacy concern, doctor personal data fetching
    email: Annotated[str, Field(default="", description="email address of the doctor")]
    phone: Annotated[str, Field(default="", description="phone number of the doctor")]
    # TODO, what?
    shift: Annotated[str, Field(...)]
    location: Annotated[str, Field(...)]

