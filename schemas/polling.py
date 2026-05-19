"""
Pydantic models for sending and receiving polling request and response
"""

from pydantic import Field, Annotated, BaseModel, ConfigDict
from core.enums import PollType


class Base(BaseModel):
    """base configuration class for all the subsequent polling classes"""

    model_config = ConfigDict(extra="fobid", str_to_lower=True, use_enum_value=True)

    poll_type: Annotated[PollType, Field(PollType.notification)]


class PollStatusRequest(Base):
    """polling class when sending a poll request to
    retrieve status from server of any pending actions"""

    pass


class PollStatusResponse(Base):
    """polling class when recieving a poll request from
    the server of any pending actions"""

    pass
