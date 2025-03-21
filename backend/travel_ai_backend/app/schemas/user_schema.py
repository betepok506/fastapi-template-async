from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from travel_ai_backend.app.models.group_model import GroupBase
from travel_ai_backend.app.models.user_model import UserBase
from travel_ai_backend.app.utils.partial import optional

from .image_media_schema import IImageMediaRead
from .role_schema import IRoleRead


class IUserCreate(UserBase):
    password: str

    class Config:
        hashed_password = None


# All these fields are optional
@optional()
class IUserUpdate(UserBase):
    pass


# This schema is used to avoid circular import
class IGroupReadBasic(GroupBase):
    id: UUID


class IUserRead(UserBase):
    id: UUID
    role: IRoleRead | None = None
    groups: list[IGroupReadBasic] | None = []
    image: IImageMediaRead | None
    follower_count: int | None = 0
    following_count: int | None = 0


class IUserReadWithoutGroups(UserBase):
    id: UUID
    role: IRoleRead | None = None
    image: IImageMediaRead | None
    follower_count: int | None = 0
    following_count: int | None = 0


class IUserBasicInfo(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class IUserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
