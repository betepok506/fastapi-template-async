from datetime import datetime
from typing import Union
from uuid import UUID

from sqlalchemy.orm import declared_attr
from sqlmodel import Field
from sqlmodel import SQLModel as _SQLModel

from travel_ai_backend.app.utils.uuid6 import uuid7


# id: implements proposal uuid7 draft4
class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__


class BaseUUIDModel(SQLModel):
    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )
    updated_at: Union[datetime, None] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
    created_at: Union[datetime, None] = Field(default_factory=datetime.utcnow)
