"""
Polling system schematics
"""

from datetime import date

from sqlalchemy import Column, Enum, ForeignKey, PrimaryKeyConstraint, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

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
        index=True,
        nullable=False,
    )

    # the target, to which the poll is propagated to
    poll_to = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        index=True,
        nullable=False,
    )

    # notification lookup and fetch priority
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
        default=list,
    )

    __table_args__ = (
        PrimaryKeyConstraint("poll_from", "poll_to", "poll_type"),
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

    id = Column(
        UInteger,
        autoincrement=True,
        nullable=False,
        primary_key=True,
        index=True,
    )

    chat_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    chat = relationship("Chats", back_populates="poll_chat_info", uselist=False)


class PollNotification(Base):
    """general notification poll, eg system propagated notifications and alerts,
    reminders etc"""

    __tablename__ = "polls_notification"

    id = Column(
        UInteger,
        autoincrement=True,
        nullable=False,
        primary_key=True,
        index=True,
    )

    poll_from = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    poll_to = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    content = Column(LowString(500), nullable=False)
    priority = Column(UInteger, nullable=False, default=5)
    read = Column(Boolean, nullable=False, default=False)
    issue_time = Column(Date, nullable=False, default=date.today)
