from uuid import UUID

from fastapi import Path, Query
from typing_extensions import Annotated

from travel_ai_backend.app.crud.role_crud import role
from travel_ai_backend.app.models.role_model import Role
from travel_ai_backend.app.utils.exceptions.common_exception import (
    IdNotFoundException,
    NameNotFoundException,
)


async def get_user_role_by_name(
    role_name: Annotated[
        str, Query(title="String compare with name or last name")
    ] = ""
) -> str:
    obj_role = await role.get_role_by_name(name=role_name)
    if not obj_role:
        raise NameNotFoundException(Role, name=role_name)
    return role_name


async def get_user_role_by_id(
    role_id: Annotated[UUID, Path(title="The UUID id of the role")]
) -> Role:
    obj_role = await role.get(id=role_id)
    if not obj_role:
        raise IdNotFoundException(Role, id=role_id)
    return obj_role
