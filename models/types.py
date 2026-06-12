"""
Wagfu backend service
custom types
Updated 8 May 2026
"""

from pydantic import ValidationError

from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import TypeDecorator

from core.types import Coordinates, FacilitatorLinks, Address

__all__ = [
    "CapString",
    "LowString",
    "UpString",
    "UInteger",
    "CoordinateJSONB",
    "SocialsJSONB",
    "AddressJSONB",
]


# type decorator base for string type
class StringType(TypeDecorator):
    impl = String
    cache_ok = True


# type decorator base for int type
class IntegerType(TypeDecorator):
    impl = Integer
    cache_ok = True


# type decorator base for JSONB type
class JSONBType(TypeDecorator):
    impl = JSONB
    cache_ok = True


class CapString(StringType):
    """
    capitalized string
    """

    # orm -> db
    def process_bind_param(self, value: str, dialect):
        return value if not value else value.capitalize()

    # db -> orm
    def process_result_value(self, value, dialect):
        return value if not value else value.lower()


class UpString(StringType):
    """
    Upper case string
    """

    def process_bind_param(self, value: str, dialect):
        return value if not value else value.upper()

    def process_result_value(self, value: str, dialect):
        return value if not value else value.upper()


class LowString(StringType):
    """
    Lowercase String
    """

    def process_bind_param(self, value: str, dialect):
        return value if not value else value.lower()

    def process_result_value(self, value: str, dialect):
        return value if not value else value.lower()


class UInteger(IntegerType):
    """
    Unsigned Integer
    """

    def process_bind_param(self, value: int, dialect):
        return 0 if value < 0 else value

    def process_result_value(self, value: int, dialect):
        return value


class CoordinateJSONB(JSONBType):
    """
    Coordinate JSONB having keys lat,lng
    and constrained values
    """

    def process_bind_param(self, value: dict, dialect):
        if value is None:
            return None

        if isinstance(value, dict):
            try:
                Coordinates(**value)  # try to create model
                return value
            except ValidationError as e:
                raise ValueError(f"Unable to parse value {value}") from e

    def process_result_value(self, value: dict, dialect):
        if value is None:
            return None

        if isinstance(value, dict):
            return Coordinates(**value)


class SocialsJSONB(JSONBType):
    """
    Social links and stuff storing jsonb
    """

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        if isinstance(value, dict):
            try:
                FacilitatorLinks(**value)
                return value
            except Exception as e:
                raise ValueError("Failed to validate FacilitatorLinks Structure") from e

    def process_result_value(self, value, dialect):
        if value is None:
            return None

        if isinstance(value, dict):
            return FacilitatorLinks(**value)


class AddressJSONB(JSONBType):
    """
    address JSONB type (core.types.address)
    """

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        if isinstance(value, dict):
            try:
                Address(**value)
                return value
            except ValidationError as e:
                raise ValueError(f"Wrong address format: {e}") from e

        if isinstance(value, Address):
            return value.model_dump()

    def process_result_value(self, value: dict, dialect):
        if value is None:
            return None

        if isinstance(value, dict):
            return Address(**value)
