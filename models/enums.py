"""
Wagfu service backend
handle orm enumeration types
Updated 7 May 2026
"""

from enum import Enum


class UserType(str, Enum):
    """types of users"""

    PET_OWNER = "owner"
    EMERGENCY = "emergency"
    DOCS = "doctor"
    ADMIN = "admin"
    PHARMA = "pharmaceuticals"


class Animals(str, Enum):
    """types of animals"""

    DOG = "dog"
    CAT = "cat"
    BRD = "bird"
    FISH = "fish"
    REP = "reptile"
    RBT = "rabbit"
    OTH = "other"
