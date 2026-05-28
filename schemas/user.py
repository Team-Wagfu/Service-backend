""" """

from pydantic import BaseModel, Annotated, Field, EmailStr
from pydantic import model_validator

from core.enums import UserType


class User(BaseModel):
    """basic user format"""

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
