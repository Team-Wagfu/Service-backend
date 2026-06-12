# Wagfu service backend
# custom annotated types
# Updated 1 May 2026

from typing import Annotated
from datetime import date
from pydantic import (
    AfterValidator,
    Field,
    TypeAdapter,
    BaseModel,
    ConfigDict,
    model_validator,
    ValidationError,
)

from core.validators import prefix, validate_link, validate_username
from core.normalise import normalise_link, normalise_username
from core.enums import AddressType

__all__ = [
    "PetID",
    "DocID",
    "PetOwnerID",
    "PharmaceuticalID",
    "ClinicID",
    "MedicalRecordID",
    "PetPassportID",
    "FacilitatorID",
    "IdTypeAdapter",
]


PetID = Annotated[str, AfterValidator(prefix("PET"))]
DocID = Annotated[str, AfterValidator(prefix("DOC"))]
PetOwnerID = Annotated[str, AfterValidator(prefix(("PW", "OWN")))]
PharmaceuticalID = Annotated[str, AfterValidator(prefix(("PHM", "FAC")))]
ClinicID = Annotated[str, AfterValidator(prefix(("CLN", "FAC")))]
MedicalRecordID = Annotated[str, AfterValidator(prefix("MED"))]
PetPassportID = Annotated[str, AfterValidator(prefix("PPA"))]
FacilitatorID = PharmaceuticalID | ClinicID


class IdTypeAdapter:
    """type adapters global shared instance collection"""

    pet = TypeAdapter(PetID)
    doc = TypeAdapter(DocID)
    petowner = TypeAdapter(PetOwnerID)
    pharma = TypeAdapter(PharmaceuticalID)
    clinic = TypeAdapter(ClinicID)
    medical = TypeAdapter(MedicalRecordID)
    petpassport = TypeAdapter(PetPassportID)
    fac = TypeAdapter(FacilitatorID)


class Coordinates(BaseModel):
    """model to store coordinates"""

    lat: Annotated[float, Field(..., ge=-90, le=90)]
    lng: Annotated[float, Field(..., ge=-180, le=180)]

    model_config = ConfigDict(extra="forbid")


class Address(BaseModel):
    address_line_1: Annotated[
        str, Field(..., description="mandatory field, primary unit identifier")
    ]
    address_line_2: Annotated[
        str, Field(default="", description="secondary information")
    ]
    street: Annotated[str, Field(..., description="street/road name")]
    locality: Annotated[str, Field(..., description="Area/neighborhood/village")]
    city: Annotated[
        str, Field(..., description="City/Town")
    ]  # should check for validity
    district: Annotated[
        str, Field(..., description="Administrative district")
    ]  # should check for validity
    state: Annotated[str, Field(..., description="state/union teritory")]
    postal_code: Annotated[int, Field(..., gt=0, description="Postal code")]
    country: Annotated[str, Field(None, description="ISO standard country code")]
    address_type: Annotated[
        AddressType,
        Field(
            default=AddressType.HOME,
            description="address type, could be home/facility location",
        ),
    ]

    model_config = ConfigDict(
        extra="ignore",
        use_enum_values=True,
        str_to_lower=True,
    )


class FacilitatorLinks(BaseModel):
    """model for public profile links"""

    website: Annotated[
        str,
        Field(
            default="",
            description="website link",
        ),
    ]
    instagram: Annotated[
        str,
        Field(
            default="",
            description="instagram username",
        ),
    ]
    facebook: Annotated[
        str,
        Field(
            default="",
            description="Facebook username",
        ),
    ]
    linkedin: Annotated[
        str,
        Field(
            default="",
            description="linkedin username",
        ),
    ]
    # other relevant links

    # other properties
    updated_at: Annotated[
        date,
        Field(
            default_factory=date.today,
            description="Date at which this corresponding set of records(links) were modified",
        ),
    ]

    # validate if the values are legitimate links
    # or follows defined username constraints and format

    @model_validator(mode="after")
    def validate_or_extract_links(self):
        """
        validate the values by checking for format
        parse and replace links with username value in place of username
        place links as in in place of links
        """

        # validate links
        try:
            # strictly web url
            validate_link(self.website)

            # validate usernames
            validate_username(self.instagram)
            validate_username(self.facebook)
            validate_username(self.linkedin)
        except Exception as e:
            raise ValidationError("Couldn't validate links") from e

        # normalise links and username
        try:
            # normalise website link
            self.website = normalise_link(self.website)

            self.instagram = normalise_username(self.instagram)
            self.facebook = normalise_username(self.facebook)
            self.linkedin = normalise_username(self.linkedin)
        except Exception as e:
            raise ValidationError("Couldn't normalise usernames") from e

        return self

    @model_validator(mode="after")
    def validate_date(self):
        """
        verify the modified date is no more that today when being set
        """

        if self.updated_at > date.today():
            raise ValueError("Update date cannot be in the future")

        return self

    model_config = ConfigDict(
        extra="forbid",
    )
