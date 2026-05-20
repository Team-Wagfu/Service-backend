"""
Wagfu service backend
model to handle chat metadata among doctors, pharmaceuticals, other facilities and the customer.

chats are identified by a 32 byte unique identifier,
metadata includes the uuid of the 2 end users, end-to-end encryption keys for the chat, etc.

Client A(initialtor) <---> Client B
users are identified by UUID, since anyone can be an initiator
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialect.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import Base
from models.types import UpString, LowString, UInteger


class Chats(Base):
    """handle chat metadata"""

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

    chat_key = Column(LowString)
