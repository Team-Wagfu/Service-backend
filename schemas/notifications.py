# Wagfu service backend
# pydantic models handling request and response of notification and alerts
# Updated 10 Jun 2026

from datetime import date
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing_extensions import Self

from schemas.enums import ReturnStatus

__all__ = [
    "Notification",
    "NotificationList",
    "NotificationAckAction",
    "NotificationAck",
    "SendNotification",
]


class NotificationModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid", use_enum_values=True, validation_error_cause=True
    )

    count: Annotated[
        int,
        Field(
            default=0,
            description="number of records returned, check status if unexpected result",
        ),
    ]
    status: Annotated[
        ReturnStatus,
        Field(
            default=ReturnStatus.error,
            description="return status whether the its successful response or error",
        ),
    ]


class Notification(BaseModel):
    id: Annotated[int, Field(..., description="notification record id")]
    poll_from: Annotated[UUID, Field(..., description="sender user id")]
    issue_time: Annotated[date, Field(default_factory=date.today)]
    content: Annotated[str, Field(..., min_length=1, max_length=500)]
    priority: Annotated[int, Field(default=5, ge=0, le=5)]
    read: Annotated[
        bool,
        Field(
            default=False,
            description="whether the notification was read(ack-ed) or not",
        ),
    ]

    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class NotificationList(NotificationModel):
    data: Annotated[
        list[Notification],
        Field(default_factory=list, description="list of notification objects"),
    ]

    @model_validator(mode="after")
    def validator_count(self) -> Self:
        if self.count != len(self.data):
            raise ValueError("inconsistency in number of notifications")
        return self

    @field_validator("data")
    @classmethod
    def validator_sort_notifications(cls, items: list[Notification]) -> list[Notification]:
        return sorted(
            items,
            key=lambda notification: (
                -notification.priority,
                notification.issue_time,
            ),
        )


class NotificationAckAction(str, Enum):
    ack = "ack"
    delete = "delete"
    ack_del = "ack-del"


class NotificationAck(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        validation_error_cause=True,
    )

    notification_id: Annotated[
        int, Field(..., description="id of the notification")
    ]
    action: Annotated[NotificationAckAction, Field(...)]


class SendNotification(BaseModel):
    """request body for dispatching a notification to another user"""

    recipient_id: Annotated[UUID, Field(..., description="target user uuid")]
    content: Annotated[str, Field(..., min_length=1, max_length=500)]
    priority: Annotated[int, Field(default=5, ge=0, le=5)]

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
