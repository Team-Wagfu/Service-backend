"""
systemwide exception definitions, to be caught by middleware
"""


class AppError(Exception):
    """Application exception superclass"""

    def __init__(self, msg: str, status_code: int = 400):
        self.msg = msg
        self.status_code = status_code
        super().__init__(msg)  # creates Exception instance


class ExpiredTokenException(AppError):
    """token timed out"""

    def __init__(self):
        super().__init__(
            msg="Expired Token, please re-authenticate", status_code=403
        )  # creates AppError instance


class InvalidSignatureException(AppError):
    """token signature mismatch"""

    def __init__(self):
        super().__init__(
            msg="Invalid Token, please re-aquire a new token", status_code=403
        )  # creates AppError instance

    # add method to note this exception
    @staticmethod
    def notify():
        """invalid signature tries should be noticed for security audit"""
        pass


class AuthenticationError(AppError):
    """auth/reg operation failure"""

    def __init__(self):
        super().__init__(
            msg="Authorization Error, please try again"
        )  # creates AppError instance


class UserExistsError(AppError):
    """user already exists"""

    def __init__(self):
        super().__init__(msg="Failed auth", status_code=401)


class PetError(AppError):
    """pet operation failure"""

    def __init__(self, msg: str = "Failed to process pet request"):
        super().__init__(msg=msg, status_code=400)


class PetNotFoundError(AppError):
    """pet record not found"""

    def __init__(self):
        super().__init__(msg="Pet not found", status_code=404)


class PetOwnerProfileError(AppError):
    """pet owner profile missing"""

    def __init__(self):
        super().__init__(msg="Pet owner profile not found", status_code=404)


class PetAccessError(AppError):
    """caller is not a pet owner"""

    def __init__(self):
        super().__init__(msg="Only pet owners can manage pets", status_code=403)


class NotificationError(AppError):
    """notification operation failure"""

    def __init__(self, msg: str = "Failed to process notification request"):
        super().__init__(msg=msg, status_code=400)


class NotificationNotFoundError(AppError):
    """notification record not found"""

    def __init__(self):
        super().__init__(msg="Notification not found", status_code=404)


class NotificationAccessError(AppError):
    """invalid notification action for caller"""

    def __init__(self):
        super().__init__(
            msg="Cannot send a notification to yourself", status_code=403
        )


class NotificationUserError(AppError):
    """authenticated user could not be resolved"""

    def __init__(self):
        super().__init__(msg="User identity not found", status_code=404)


class PetAddonError(AppError):
    """vaccination or medical record operation failure"""

    def __init__(self, msg: str = "Failed to process pet health record request"):
        super().__init__(msg=msg, status_code=400)


class PetAddonAccessError(AppError):
    """caller lacks permission for pet health records"""

    def __init__(self, msg: str = "Access denied for pet health records"):
        super().__init__(msg=msg, status_code=403)


class VaccinationNotFoundError(AppError):
    """vaccination record not found"""

    def __init__(self):
        super().__init__(msg="Vaccination record not found", status_code=404)


class MedicalRecordNotFoundError(AppError):
    """medical record not found"""

    def __init__(self):
        super().__init__(msg="Medical record not found", status_code=404)


# export
__all__ = [
    "ExpiredTokenException",
    "InvalidSignatureException",
    "AuthenticationError",
    "UserExistsError",
    "PetError",
    "PetNotFoundError",
    "PetOwnerProfileError",
    "PetAccessError",
    "NotificationError",
    "NotificationNotFoundError",
    "NotificationAccessError",
    "NotificationUserError",
    "PetAddonError",
    "PetAddonAccessError",
    "VaccinationNotFoundError",
    "MedicalRecordNotFoundError",
]
