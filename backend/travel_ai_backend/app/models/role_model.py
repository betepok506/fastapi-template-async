from sqlmodel import Relationship, SQLModel

from travel_ai_backend.app.models.base_uuid_model import BaseUUIDModel


class RoleBase(SQLModel):
    name: str
    description: str


class Role(BaseUUIDModel, RoleBase, table=True):
    users: list["User"] = Relationship(  # noqa: F821
        back_populates="role", sa_relationship_kwargs={"lazy": "selectin"}
    )
