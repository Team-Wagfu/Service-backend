"""
systemwide exception definitions
"""


class InvalidActionException(Exception):
    """for parser internal actions"""


class TemplateFileError(Exception):
    """for handling template file related errors"""


class NormalisationFailureWarning(Exception):
    """raised when normalisation functions fail"""


__all__ = ["InvalidActionException"]
