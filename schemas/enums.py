# Waguf service backend
# common utilities and enumeration classes
# Updated 26 Apr 2026

from enum import Enum

# enumeration to mark status of response
class ReturnStatus(str, Enum):
    success="success"
    error="error"
