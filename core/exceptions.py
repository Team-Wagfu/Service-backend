"""
systemwide exception definitions
"""


class InvalidActionException(Exception):
    """for parser internal actions"""


class TemplateFileError(Exception):
    """for handling template file related errors"""


__all__ = ["InvalidActionException"]
