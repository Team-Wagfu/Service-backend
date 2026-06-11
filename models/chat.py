"""
Wagfu service backend
model to handle chat metadata among doctors, pharmaceuticals, other facilities and the customer.

chats are identified by a 32 byte unique identifier,
metadata includes the uuid of the 2 end users, end-to-end encryption keys for the chat, etc.

Client A(initialtor) <---> Client B
users are identified by UUID, since anyone can be an initiator
"""

from datetime import date

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base
from models.types import LowString
from services.jwt.helper import create_32_hex


class Chats(Base):
    """handle chat metadata"""

    __tablename__ = "chats"

    # chat_id is now the sole primary key
    chat_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    # client A, the chat initiator (primary_key=True removed)
    peer_client = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
    )

    # client B (primary_key=True removed)
    peer_server = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=True,
    )

    # end-to-end encryption key
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
        "PollChatNotification", back_populates="chat", uselist=False
    )

    # If we ever want to ensure the same two users can't initiate 
    # multiple duplicate chat records, uncomment the lines below:
    # __table_args__ = (
    #     UniqueConstraint("peer_client", "peer_server", name="uq_chat_peers"),
    # )


__all__ = ["Chats"]