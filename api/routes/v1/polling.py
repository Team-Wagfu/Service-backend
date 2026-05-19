"""
short polled matchmaker routes
facilitating connection request from the client A,
facilitating access to data from client B for persistent polling and data collection

Polling system for both
    - notifications
    - call(matchmaking)

SECURITY UNIMPLEMENTED YET
"""

from fastapi import APIRouter
from fastapi import Body, Depends


from schemas.polling import *

router = APIRouter(
    prefix="/poll",
    tags=["poll", "audio-routing", "notification-routing", "routing"],
)
