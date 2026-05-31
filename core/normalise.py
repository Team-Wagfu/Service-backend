"""
Wagfu Service backend
normalisation functions
Updated 16 May 2026
"""

from urllib.parse import urlsplit, ParseResult


def normalise_link(link: str) -> str:
    """given the validated link string,
    parsed and normalised form of the string link is returned
    """

    if not link:
        return ""

    try:
        parsed: ParseResult = urlsplit(link if "://" in link else f"//{link}")
        return f"{parsed.hostname}{parsed.path}".lower()

    except Exception as e:
        raise ValueError("Couldn't parse string url") from e


def normalise_username(username: str) -> str:
    """given the username string, return the normalised username"""

    if not username:
        return ""

    return username.strip(" @\n").lower()
