import hmac
import hashlib
import base64
import json
import time

from config import config


def b64_urlencode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64_urldecode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data * padding)


def sign(data: str) -> str:
    signature = hmac.new(
        config.JWT_SECRET.encode(), data.encode(), hashlib.sha256
    ).digest()

    return b64_urlencode(signature)


def create_jwt(payload: dict) -> str:
    header = {
        "alg": "HS256",
        "typ": "JWT",
    }

    encoded_header = b64_urlencode(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = b64_urlencode(json.dumps(payload, separators=(",", ":")).encode())

    data = f"{encoded_header}.{encoded_payload}"
    signature = sign(data)

    return f"{data}.{signature}"


def verify_jwt(token: str, secret: str):
    header_b64, payload_b64, signature = token.split(".")

    data = f"{header_b64}.{payload_b64}"

    expected_signature = sign(data, secret)

    if not hmac.compare_digest(signature, expected_signature):
        raise Exception("Invalid signature")

    payload = json.loads(b64_urldecode(payload_b64))

    if payload["exp"] < int(time.time()):
        raise Exception("Token expired")

    return payload
