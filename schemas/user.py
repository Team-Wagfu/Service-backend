""" """

from pydantic import BaseModel, Annotated, Field, EmailStr
from pydantic import model_validator

from core.types import PetOwnerID, FacilitatorID, DocID
from core.enums import UserType


class createUser(BaseModel):
    """basic user format, used when creating and updating a user"""

    name: Annotated[str, Field(..., min_length=3, max_length=50)]
    email: Annotated[EmailStr, Field(...)]
    pwd: Annotated[str, Field(..., min_length=8, max_length=100)]
    pwd_cnf: Annotated[str, Field(..., min_length=8, max_length=100)]

    type: Annotated[UserType, Field(...)]

    @model_validator(mode="after")
    def validate_pwd_match(self):
        if self.pwd != self.pwd_cnf:
            raise ValueError("passwords do not match")
        return self


class loginUser(BaseModel):
    """credentials used when logging in"""

    email: Annotated[EmailStr, Field(...)]
    pwd: Annotated[str, Field(..., min_length=8, max_length=100)]


class readUser(BaseModel):
    """model when reading a user data"""

    name: str
    email: EmailStr
    profile_id: PetOwnerID | FacilitatorID | DocID
    profile_type: str
    token: str
