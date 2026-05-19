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
        if not value.startswith(prefix):
            raise ValueError(f"Id should start with {p}")

        sectors = value.split("-")[1:]
        if not (sectors[0].isdigit() and sectors[1].isdigit()):
            raise ValueError(f"Id parse failure, format error, prefix: {value}, l1")

        if len(sectors[-1]) != 5 or len(sectors[0]) != 4 or len(sectors) != 2:
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

    cleaned = re.sub(r"[\s\-$$$$]", "", v)

    if not cleaned.isdigit():
        raise ValueError("Phone number must contain only digits")

    if len(cleaned) != 10:
        raise ValueError("Phone number must be 10 digits")

    if not re.match(r"^(\+91|0)?[6-9]\d{9}$", cleaned):
        raise ValueError("Invalid Phone number")

    return cleaned


SOCIAL_PATTERN = (
    r"^(?P<is_username>@(?P<username>[a-zA-Z0-9._]{1,30}))|"
    r"(?P<is_url>https?://(?P<website>(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)))$"
)


def validate_link(link: str) -> str:
    """validate the given string for link/url format
    and raise exception if failed
    """

    if not link:
        return link

    matched_link = re.match(SOCIAL_PATTERN, link)
    if not matched_link:
        raise ValueError("Provided string doesn't adhere to standard url format")

    # check if matched against is_url format
    if not matched_link.group("is_url"):
        # shouldn't occur
        raise ValueError("failed to parse usl from given format")

    return link


def validate_username(username: str) -> str:
    """validate the given string for username format
    often times prepended with '@'
    """

    if not username:
        return username

    matched_username = re.match(SOCIAL_PATTERN, username)
    if not matched_username:
        raise ValueError("Provided username doesnt follow username format")

    if not matched_username.group("is_username"):
        # shouldn't occur, this too
        raise ValueError("Failed to parse username from given format")

    return username
