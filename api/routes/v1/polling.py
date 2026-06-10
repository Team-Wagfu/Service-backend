"""
Short polled notification routes.

Client A dispatches notifications; client B polls on an interval for pending work.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, status
from sqlalchemy.orm import Session

from db.dependencies import get_db
from schemas.notifications import (
    Notification,
    NotificationAck,
    NotificationList,
    SendNotification,
)
from schemas.polling import PollStatusRequest, PollStatusResponse
from services.jwt.master import user_metadata
from services.notification import NotificationService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("Starting /poll router")
router = APIRouter(
    prefix="/poll",
    tags=["poll", "notification-routing"],
)


@router.get("/status", response_model=PollStatusResponse, status_code=status.HTTP_200_OK)
async def poll_status(
    poll_type: Annotated[int | None, Query(description="optional PollType filter")] = None,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    request = PollStatusRequest(poll_type=poll_type)
    return NotificationService.poll_status(
        request,
        user.get("profile_id", ""),
        session,
    )


@router.post(
    "/notification/send",
    response_model=Notification,
    status_code=status.HTTP_201_CREATED,
)
async def send_notification(
    payload: Annotated[SendNotification, Body(...)],
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    logger.debug(
        "dispatching notification from %s to %s",
        user.get("profile_id"),
        payload.recipient_id,
    )
    return NotificationService.send(
        payload,
        user.get("profile_id", ""),
        session,
    )


@router.get(
    "/notification/list",
    response_model=NotificationList,
    status_code=status.HTTP_200_OK,
)
async def list_notifications(
    unread_only: Annotated[bool, Query()] = False,
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return NotificationService.list_notifications(
        user.get("profile_id", ""),
        session,
        unread_only=unread_only,
    )


@router.post(
    "/notification/ack",
    response_model=Notification | None,
    status_code=status.HTTP_200_OK,
)
async def acknowledge_notification(
    payload: Annotated[NotificationAck, Body(...)],
    user=Depends(user_metadata),
    session: Session = Depends(get_db),
):
    return NotificationService.acknowledge(
        payload,
        user.get("profile_id", ""),
        session,
    )
