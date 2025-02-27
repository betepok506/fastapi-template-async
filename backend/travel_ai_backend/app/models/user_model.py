from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy_utils import ChoiceType
from sqlmodel import (
    BigInteger,
    Column,
    DateTime,
    Field,
    Relationship,
    SQLModel,
    String,
)

from travel_ai_backend.app.models.base_uuid_model import BaseUUIDModel
from travel_ai_backend.app.models.image_media_model import ImageMedia
from travel_ai_backend.app.models.links_model import LinkGroupUser
from travel_ai_backend.app.schemas.common_schema import IGenderEnum

# from travel_ai_backend.app.models.base_uuid_model import BaseUUIDModel
# from travel_ai_backend.app.models.image_media_model import ImageMedia
# from travel_ai_backend.app.models.links_model import LinkGroupUser
# from travel_ai_backend.app.schemas.common_schema import IGenderEnum


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    birthdate: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )  # birthday with timezone
    role_id: UUID | None = Field(default=None, foreign_key="Role.id")
    phone: str | None = None
    gender: IGenderEnum | None = Field(
        default=IGenderEnum.other,
        sa_column=Column(ChoiceType(IGenderEnum, impl=String())),
    )
    state: str | None = None
    country: str | None = None
    address: str | None = None


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str | None = Field(
        default=None, nullable=False, index=True
    )
    role: Optional["Role"] = Relationship(  # noqa: F821
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )
    groups: list["Group"] = Relationship(  # noqa: F821
        back_populates="users",
        link_model=LinkGroupUser,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    image_id: UUID | None = Field(default=None, foreign_key="ImageMedia.id")
    image: ImageMedia = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "User.image_id==ImageMedia.id",
        }
    )
    follower_count: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    following_count: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
