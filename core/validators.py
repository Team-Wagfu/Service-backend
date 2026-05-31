"""
Validator perform only verification if the value is fit for as per the given
constraints and doesn't conduct any normalisation,

if valid and follows the given conditions, it will return the same object
if not valid, it will raise and exception
"""

from typing import Callable
import re


__all__ = [
    "prefix",  # for id types
    "phone_number_validator",
    "validate_link",  # validate links all throughout the api
    "validate_username",  # validate username all throughout the api
]


# validator for id prefix
def prefix(p: str) -> Callable[[str], str]:
    """generates a validator function object
    that validated if the given string satisfies the given conditions
    along with the given prefix

    Example:
            prefix('abc') -> function

            function: verifies if the passed string starts with the given prefix
            and follows the given format prefix-[4 digit]-[5 digit]
    """

    def validator(value: str) -> str | None:
        if value == "":
            return value

        if not value.startswith(p):
            raise ValueError(f"Id should start with {p}")

        sectors = value.split("-")[1:]
        if len(sectors) != 2:
            raise ValueError(f"Id parse failure, format error, prefix: {value}, l1")

        if not (sectors[0].isdigit() and sectors[1].isdigit()):
            raise ValueError(f"Id parse failure, format error, prefix: {value}, l1")

        if len(sectors[-1]) != 5 or len(sectors[0]) != 4:
            raise ValueError(f"Id parse failure, format error, prefix: {value}, l2")

        if not int(sectors[-1]):
            raise ValueError("Invalid ID, 00000")

        return value

    return validator


# validate phone number
def phone_number_validator(v: str) -> str:  # TODO
    """verify if the given phone number is valid or not
    checking thru patterns to see if any of it matches
    """

    cleaned = re.sub(r"[\s\-]", "", v)

    if not cleaned:
        return True

    if cleaned.startswith("+91"):
        cleaned = cleaned[3:]
    elif cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]

    if not cleaned.isdigit():
        raise ValueError("Phone number must contain only digits")

    if len(cleaned) != 10:
        raise ValueError("Phone number must be 10 digits")

    if cleaned.startswith("0"):
        raise ValueError("Invalid Phone number")

    return cleaned


LINK_PATTERN = (
    r"^(?:https://)?(?:www\.)?"
    r"[-a-zA-Z0-9@:%._+~#=]{1,256}"
    r"\.[a-zA-Z0-9()]{1,6}\b"
    r"(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$"
)
USERNAME_PATTERN = r"^@[a-zA-Z0-9._]{1,30}$"


def validate_link(link: str) -> str:
    """validate the given string for link/url format
    and raise exception if failed
    """

    if not link:
        return True

    matched_link = re.match(LINK_PATTERN, link)
    if not matched_link:
        raise ValueError("Provided string doesn't adhere to standard url format")

    return link


def validate_username(username: str) -> str:
    """validate the given string for username format
    often times prepended with '@'
    """

    if not username:
        return True

    matched_username = re.match(USERNAME_PATTERN, username)
    if not matched_username:
        raise ValueError("Provided username doesnt follow username format")

    return username
