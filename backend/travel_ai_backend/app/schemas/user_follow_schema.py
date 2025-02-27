from uuid import UUID

from pydantic import BaseModel

from travel_ai_backend.app.models.user_follow_model import UserFollowBase
from travel_ai_backend.app.utils.partial import optional


class IUserFollowCreate(UserFollowBase):
    pass


# All these fields are optional
@optional()
class IUserFollowUpdate(UserFollowBase):
    pass


class IUserFollowRead(UserFollowBase):
    is_mutual: bool


class IUserFollowReadCommon(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    follower_count: int
    following_count: int
    is_mutual: bool
