"""
Wagfu service backend
handle orm enumeration types
Updated 7 May 2026
"""

from core.enums import UserType, Animals, FacilityType
from sqlalchemy import Enum

__all__ = ["UserTypeEnum", "AnimalsEnum", "FacilityTypeEnum"]

UserTypeEnum = Enum(
    UserType,
    values_callable=lambda obj: [x.value for x in obj],  # to prevent use of enum keys
)

AnimalsEnum = Enum(
    Animals,
    values_callable=lambda obj: [x.value for x in obj],
)

FacilityTypeEnum = Enum(
    FacilityType,
    values_callable=lambda obj: [x.value for x in obj],
)
