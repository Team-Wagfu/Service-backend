# Wagfu service backend
# profile schemas for defining request response pydantic models
# Updated 29 May 2026

from typing import Annotated, Optional
from uuid import uuid4, UUID

from pydantic import Field, BaseModel, ConfigDict

from core.types import Address, FacilitatorLinks
from core.types import PetOwnerID, DocID, FacilitatorID, PetID
from core.enums import FacilityType


# put models
class WriteConfig(BaseModel):
    # user_id is filled automatically at insertion site
    # id is automatically populated at the insertion site

    # common fields

    # from the users table
    user_id: UUID

    # in case of registration, the user_id is intentionally
    # left empty as the user doesnt aquire an id by that time
    # for the forcoming requests, the user_id field shall be
    # filled, for further contextwise actions
    # hence the field is left as optional
    # the empty string shall be handled at the CRUD layer
    id: Annotated[PetOwnerID | DocID | FacilitatorID, Field(default="")]

    location: Annotated[dict, Field(..., description="coordinates of the user")]

    address: Annotated[
        Address,
        Field(
            ...,
            description="detailed address, see core.types.Address for more info on the fields",
        ),
    ]

    # configuration for write models
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )


class WritePetOwnerProfile(WriteConfig):
    # address here recieved in case of emergency or immediate
    # dispatch location mapping
    pet_ids: Annotated[
        list[str],
        Field(default_factory=list, description="Pet ids of pets owned by the user"),
    ]


class WriteDoctorProfile(WriteConfig):
    # address, in this context means, clinic location
    # assuming everyone runs their own clinic,
    # make the address part optional here TODO
    specialisation: Annotated[str, Field(..., max_length=50)]
    experience: Annotated[int, Field(default=0, ge=0, le=100)]


class WriteAdminProfile(WriteConfig):
    pass


class WriteFacilitatorProfile(WriteConfig):
    # address, in this context is the address of the
    # facility
    name: Annotated[str, Field(..., min_length=1, max_length=100)]
    description: Annotated[str, Field(..., max_length=150)]
    type: Annotated[FacilityType, Field(...)]
    links: Annotated[FacilitatorLinks, Field(default_factory=FacilitatorLinks)]


class ReadConfig(BaseModel):
    # common fieilds
    id: PetOwnerID | FacilitatorID | DocID

    address: Annotated[Address, Field(default_factory=Address)]

    model_config = ConfigDict(
        extra="ignore",
        strip_whitespace=True,
    )


class ReadPetOwnerProfile(ReadConfig):
    pet_ids: Annotated[list[PetID], Field(default_factory=list)]


class ReadDoctorProfile(ReadConfig):
    specialisation: Annotated[str, Field(default="")]
    experience: Annotated[int, Field(default=0)]
    rating: int
    rating_count: int


class ReadFacilitatorProfile(ReadConfig):
    name: str
    description: Annotated[str, Field(default="")]
    links: Annotated[FacilitatorLinks, Field(default_factory=FacilitatorLinks)]


# when the user wants to edit their profile
class UpdateConfig(BaseModel):
    # common fields
    id: PetOwnerID | DocID | FacilitatorID  # strict field


class UpdatePetOwnerProfile(UpdateConfig):
    # every field is optional
    address: Optional[Address]
    pet_ids: Optional[list[PetID]]


class UpdateDoctorProfile(UpdateConfig):
    # every field is optional
    specialisation: Optional[str]
    experience: Optional[int]


class UpdateFacilitatorProfile(UpdateConfig):
    # every field is optional
    name: Optional[str]
    description: Annotated[str, Field(None, max_length=150)]
    address: Optional[Address]
    type: Optional[FacilityType]
    links: Optional[FacilitatorLinks]
