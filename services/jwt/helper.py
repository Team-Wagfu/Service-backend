"""
Security architecure helper functions and classes
JWT builder components/primitives
"""

import hmac
import hashlib
import base64
import json
import time
import secrets

from config import config
from core.exceptions import ExpiredTokenException, InvalidSignatureException


def b64_urlencode(data: bytes) -> str:
    """url safe base64 encoding"""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64_urldecode(data: str) -> bytes:
    """url safe base64 decoding"""
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data * padding)


def sign(data: str, secret: str = config.JWT_SECRET) -> str:
    """sign data with the provided key"""
    signature = hmac.new(
        bytes(secret, encoding="utf-8"), data.encode(), hashlib.sha256
    ).digest()

    return b64_urlencode(signature)


def create_jwt(payload: dict) -> str:
    """create the jwt token, and return the token string"""
    header = {
        "alg": "HS256",
        "typ": "JWT",
    }

    encoded_header = b64_urlencode(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = b64_urlencode(json.dumps(payload, separators=(",", ":")).encode())

    data = f"{encoded_header}.{encoded_payload}"
    signature = sign(data)

    return f"{data}.{signature}"


def verify_jwt(token: str, secret: str = config.JWT_SECRET):
    """verify the validity of provided token(token-string)"""
    header_b64, payload_b64, signature = token.split(".")

    data = f"{header_b64}.{payload_b64}"

    expected_signature = sign(data, secret)

    if not hmac.compare_digest(signature, expected_signature):
        raise InvalidSignatureException()

    payload = json.loads(b64_urldecode(payload_b64))

    if payload["exp"] < int(time.time()):
        raise ExpiredTokenException()

    return payload


def create_32_hex():
    """create hex string of 32 characters"""
    return secrets.token_hex(32)


def create_n_hex(n=32):
    """create hex string of n characters"""
    return secrets.token_hex(n)


# export functions
__all__ = [
    "b64_urlencode",
    "b64_urldecode",
    "create_jwt",
    "verify_jwt",
    "create_32_hex",
    "create_n_hex",
    "sign",
]
