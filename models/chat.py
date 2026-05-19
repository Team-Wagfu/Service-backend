'''
Wagfu service backend
model to handle chat metadata among doctors, pharmaceuticals, other facilities and the customer.

chats are identified by a 32 byte unique identifier, 
metadata includes the uuid of the 2 end users, end-to-end encryption keys for the chat, etc.
'''

from sqlalchemy import Column
from sqlalchemy.dialect.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import Base
from models.types import UpString, LowString, UInteger

class Chats(Base):
  """handle chat metadata"""

    client = Column(
        UUID(as_uuid=True),
        ForeignKe("users.user_id"),
        primary_key=True,
        index=True,
        nullable=False,
    )

    
