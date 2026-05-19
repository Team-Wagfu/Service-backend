"""
Polling system schematics
"""

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from models.types import UInteger, LowString
from models.base import Base
from core.enums import PollType


class Polls(Base):
    """polls 'from' and 'to' and their corresponding type and priority are saved"""

    __tablename__ = "polls"

    # the poll source, of type uuid
    # either the system sends, or a particular user sends
    poll_from = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
        index=True,
        nullable=False,
    )

    # the target, to which the poll is propagated to
    poll_to = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
        index=True,
        nullable=False,
    )

    # notification lookup and fetch priority
    # 1 - call, 2 - chat, 3 - notification
    poll_type = Column(
        Enum(PollType),
        nullable=False,
    )

    # number of polls to be collected in that particular category(chat, notif, call)
    poll_count = Column(
        UInteger,
        nullable=False,
        default=1,
    )

    poll_id = Column(
        ARRAY(UInteger),
        nullable=False,
        default=[],
    )


class PollCallNotification(Base):
    """call poll"""

    __tablename__ = "polls_calls"

    id = Column(
        UInteger,
        autoincrement=True,
        primary_key=True,
    )

    # other relevant fields,
    # probably like the SDI Fields or somethin


class PollChatNotification(Base):
    """chat poll"""

    __tablename__ = "polls_chat"

    # unique identified for the record
    id = Column(
        UInteger,
        nullable=False,
        primary_key=True,
    )

    chat_id = Column(
        LowString(32),  # 32 byte unique key identifying a chat between 2 users
        nullable=False,
    )


class PollNotification(Base):
    """general notification poll, eg system propagated notifications and alerts,
    reminders etc"""

    __tablename__ = "polls_notification"
