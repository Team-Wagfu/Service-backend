"""
Wagfu service backend
model to handle chat metadata among doctors, pharmaceuticals, other facilities and the customer.

chats are identified by a 32 byte unique identifier,
metadata includes the uuid of the 2 end users, end-to-end encryption keys for the chat, etc.

Client A(initialtor) <---> Client B
users are identified by UUID, since anyone can be an initiator
"""

from datetime import date

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base
from models.types import LowString
from services.jwt.helper import create_32_hex


class Chats(Base):
    """handle chat metadata"""

    __tablename__ = "chats"

    chat_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    # client A, the chat initiator
    peer_client = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
        nullable=False,
    )

    # client B
    peer_server = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
        nullable=True,
    )

    # end-t-end ecryption key
    chat_key = Column(
        LowString,
        nullable=False,
        default=create_32_hex,
    )

    # chat initiation date
    start_date = Column(
        Date,
        default=date.today,
        nullable=False,
    )

    # if the chat has been inactive for more than 5 days
    active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    poll_chat_info = relationship(
        "PollChatNotifications", back_populates="chat_chat", uselist=False
    )


__all__ = ["Chats"]
