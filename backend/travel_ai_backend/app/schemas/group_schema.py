from uuid import UUID

from travel_ai_backend.app.models.group_model import GroupBase
from travel_ai_backend.app.utils.partial import optional

from .user_schema import IUserReadWithoutGroups


class IGroupCreate(GroupBase):
    pass


class IGroupRead(GroupBase):
    id: UUID


class IGroupReadWithUsers(GroupBase):
    id: UUID
    users: list[IUserReadWithoutGroups] | None = []


# All these fields are optional
@optional()
class IGroupUpdate(GroupBase):
    pass
