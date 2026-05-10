"""
Wagfu backend service
custom types
Updated 8 May 2026
"""

from sqlalchemy import String, Integer
from sqlalchemy import TypeDecorator

# from core.types import IdTypeAdapter

__all__ = ["CapString", "LowString", "UpString", "UInteger"]


# type decorator base for string type
class StringType(TypeDecorator):
    impl = String
    cache_ok = True


# type decorator base for int type
class IntegerType(TypeDecorator):
    impl = Integer
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
