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


# export
__all__ = ["ExpiredTokenException", "InvalidSignatureException", "AuthenticationError"]
