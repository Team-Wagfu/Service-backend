# Wagfu service backend
# pydantic models handling request and response of notification and alerts
# Updated 26 Apr 2026

#---------------------------------------------------------------------#
# ALL MODELS ARE IN DEBUG CONFIGURATION, NEED TO SWITCH TO PRODUCTION #
#---------------------------------------------------------------------#

from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator
from typing import TypedDict
from typing_extensions import Self
from enum import Enum

from .enums import ReturnStatus

__all__=["Notification", "NotificationList", "NotificationAckAction", "NotificationAck"]

# reponse model

# configuration base class for all the subsequent response classes
# !! DEBUG CODE !!
class NotificationModel(BaseModel):
    model_config=ConfigDict(
        extra='forbid',
        use_enum_values=True,
        validation_error_cause=True
    )

    count: Annotated[int, Field(default=0, description="number of records returned, check status if unexpected result")]
    status: Annotated[ReturnStatus, Field(default=ReturnStatus.error, description="return status whether the its successful response or error")]
    # _reason: Annotated[str, Field(default='', description="reason for the error, if any")]


# data dict for notification
class Notification(TypedDict):
    id: Annotated[int, Field(default=0, description="identification for the notification, local to doc")]
    issue_time: Annotated[datetime.date, Field(default_factory=datetime.date)]
    content: Annotated[int, Field(..., min_length=10, max_length=50)]
    priority: Annotated[int, Field(default=5, ge=0, le=5)]
    read: Annotated[bool, Field(default=False, description="whether the notification was read(ack-ed) or not")]

# return the list of all alerts or notifications for the doctor
class NotificationList(NotificationModel):
    data: Annotated[
        list[Notification], # list of notifications of the above specified format
        Field(default=list, description="list of norification dict object")
    ]

    @model_validator(mode='after')
    def validator_count(self) -> Self:
        if self.count!=data.__len__():
            raise ValueError('inconsistency in number of notifications')
        return self

    @field_validator('data')
    @classmethod
    def validator_sort_notifications(self, l: list[Notifications]) -> list[Notifications]:
        # sort the notification in the decreasing order of priority
        return sorted(l, key=lambda notification: notification['issue_time'], notification['priority'])


# notification acknowledgement action enumeration
class NotificationAckAction(Enum, str):
    ack="ack"            # acknowledge, mark as read, keep the Notifications
    delete="delete"      # delete, status insignificant
    ack_del="ack-del"    # ack and delete (fallback)

# notification read acknowledgement request (POST)
class NotificationAck(BaseModel):
    model_config=ConfigDict(
        extra='forbid',
        use_enum_values=True,
        validation_error_cause=True,
    )
    
    notification_id: Annotated[int, Field(default=0, description="id of the notification")]
    action: Annotated[NotificationAckAction, Field(...)]
