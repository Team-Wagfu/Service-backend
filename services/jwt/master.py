"""
Wagfu Security

JWT Token engine
"""

import logging
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.jwt.helper import verify_jwt

# setup logging
logger = logging.getLogger(__name__)

logger.info("Initialising security_model")
security_model = HTTPBearer(description="Wagfu Token bearer", auto_error=True)


async def user_metadata(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_model)],
):
    token = credentials.credentials
    scheme = credentials.scheme

    logger.debug(f"credentials: {scheme}::{token}")

    return verify_jwt(token)


__all__ = ["user_metadata"]
