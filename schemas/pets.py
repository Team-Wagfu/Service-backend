# Wagfu Service Backend
# pet data retrieval and manipulation models
# Updated 10 Jun 2026

from enum import Enum
from typing import Annotated, Optional, TypedDict

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.enums import Animals
from core.types import PetID
from models.pet_validator import SPECIES_BREED_COLOR_MAP


class ResponseStatus(str, Enum):
    success = "success"
    error = "error"


# response models
class PatientResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_to_lower=True,
        str_strip_whitespace=True,
        title="PatientResponse BaseClass",
    )

    count: Annotated[int, Field(default=0, description="number of patients")]
    status: Annotated[
        ResponseStatus,
        Field(default=ResponseStatus.error, description="status of the Response"),
    ]


class Patient(TypedDict):
    pet_name: Annotated[str, Field(...)]
    pet_id: Annotated[PetID, Field(...)]


class PatientList(PatientResponse):
    data: Annotated[
        list[Patient], Field(default_factory=list, description="list of pets")
    ]


class createPet(BaseModel):
    """payload for registering a new pet under the authenticated owner"""

    name: Annotated[str, Field(..., min_length=1, max_length=50)]
    type: Annotated[Animals, Field(...)]
    breed: Annotated[str, Field(..., min_length=1, max_length=50)]
    color: Annotated[str, Field(..., min_length=1, max_length=50)]
    weight: Annotated[int, Field(..., ge=0)]
    height: Annotated[int, Field(..., ge=0)]

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        use_enum_values=True,
    )

    @model_validator(mode="after")
    def validate_breed_and_color(self):
        animal_type = (
            self.type if isinstance(self.type, Animals) else Animals(self.type)
        )
        species_map = SPECIES_BREED_COLOR_MAP.get(animal_type)
        if species_map is None:
            return self

        if self.breed not in species_map:
            raise ValueError(f"Invalid breed '{self.breed}' for animal type '{self.type}'")

        if self.color not in species_map[self.breed]:
            raise ValueError(
                f"Invalid color '{self.color}' for breed '{self.breed}'"
            )

        return self


class readPet(BaseModel):
    """single pet record returned to the client"""

    pet_id: PetID
    owner_id: Annotated[str, Field(..., description="pet owner profile id")]
    name: str
    type: Animals
    breed: str
    color: str
    weight: int
    height: int

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
        use_enum_values=True,
    )


class updatePet(BaseModel):
    """partial update payload; pet_id identifies the target record"""

    pet_id: PetID
    name: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None
    breed: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None
    color: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None
    weight: Optional[Annotated[int, Field(ge=0)]] = None
    height: Optional[Annotated[int, Field(ge=0)]] = None

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )
