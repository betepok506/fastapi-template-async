from uuid import UUID

from fastapi import Path, Query
from typing_extensions import Annotated

from travel_ai_backend.app.crud.group_crud import group
from travel_ai_backend.app.models.group_model import Group
from travel_ai_backend.app.utils.exceptions.common_exception import (
    IdNotFoundException,
    NameNotFoundException,
)


async def get_group_by_name(
    group_name: Annotated[
        str, Query(description="String compare with name or last name")
    ] = ""
) -> str:
    obj_group = await group.get_group_by_name(name=group_name)
    if not obj_group:
        raise NameNotFoundException(Group, name=group_name)
    return obj_group


async def get_group_by_id(
    group_id: Annotated[UUID, Path(description="The UUID id of the group")]
) -> Group:
    obj_group = await group.get(id=group_id)
    if not obj_group:
        raise IdNotFoundException(Group, id=group_id)
    return obj_group
