from typing import Union
from uuid import UUID

from sqlmodel import Field

from travel_ai_backend.app.models.base_uuid_model import BaseUUIDModel


class LinkGroupUser(BaseUUIDModel, table=True):
    group_id: Union[UUID, None] = Field(
        default=None, nullable=False, foreign_key="Group.id", primary_key=True
    )
    user_id: Union[UUID, None] = Field(
        default=None, nullable=False, foreign_key="User.id", primary_key=True
    )
