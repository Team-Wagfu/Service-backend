"""
Pydantic models for sending and receiving polling request and response
"""

from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from core.enums import PollType
from schemas.enums import ReturnStatus


class PollBase(BaseModel):
    """base configuration class for all the subsequent polling classes"""

    model_config = ConfigDict(extra="forbid", str_to_lower=True, use_enum_values=True)


class PollStatusRequest(PollBase):
    """optional filter when polling the server for pending actions"""

    poll_type: Annotated[
        Optional[PollType],
        Field(default=None, description="filter by poll category when set"),
    ]


class PollEntry(BaseModel):
    """one pending poll bucket from a specific sender"""

    poll_from: UUID
    poll_type: PollType
    poll_count: Annotated[int, Field(ge=0)]
    poll_ids: Annotated[list[int], Field(default_factory=list)]

    model_config = ConfigDict(use_enum_values=True)


class PollStatusResponse(BaseModel):
    """aggregated pending poll state returned to a polling client"""

    count: Annotated[int, Field(default=0, ge=0)]
    status: Annotated[ReturnStatus, Field(default=ReturnStatus.success)]
    pending: Annotated[list[PollEntry], Field(default_factory=list)]

    model_config = ConfigDict(use_enum_values=True)
