from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Params

from travel_ai_backend.app.crud.group_crud import group
from travel_ai_backend.app.api import deps
from travel_ai_backend.app.deps import group_deps, user_deps
from travel_ai_backend.app.models.group_model import Group
from travel_ai_backend.app.models.user_model import User
from travel_ai_backend.app.schemas.group_schema import (
    IGroupCreate,
    IGroupRead,
    IGroupReadWithUsers,
    IGroupUpdate,
)
from travel_ai_backend.app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from travel_ai_backend.app.schemas.role_schema import IRoleEnum
from travel_ai_backend.app.utils.exceptions import (
    IdNotFoundException,
    NameExistException,
)

router = APIRouter()


@router.get("")
async def get_groups(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IGroupRead]:
    """
    Gets a paginated list of groups
    """
    groups = await group.get_multi_paginated(params=params)
    return create_response(data=groups)


@router.get("/{group_id}")
async def get_group_by_id(
    group_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IGroupReadWithUsers]:
    """
    Gets a group by its id
    """
    obj_out = await group.get(id=group_id)
    if obj_out:
        return create_response(data=obj_out)
    else:
        raise IdNotFoundException(Group, group_id)


@router.post("")
async def create_group(
    obj_in: IGroupCreate,
    current_user: User = Depends(
        deps.get_current_user(
            required_roles=[IRoleEnum.admin, IRoleEnum.manager]
        )
    ),
) -> IPostResponseBase[IGroupRead]:
    """
    Creates a new group

    Required roles:
    - admin
    - manager
    """
    obj_out = await group.get_group_by_name(name=obj_in.name)
    if obj_out:
        raise NameExistException(Group, name=obj_in.name)
    new_group = await group.create(
        obj_in=obj_in, created_by_id=current_user.id
    )
    return create_response(data=new_group)


@router.put("/{group_id}")
async def update_group(
    obj_in: IGroupUpdate,
    current_group: Group = Depends(group_deps.get_group_by_id),
    current_user: User = Depends(
        deps.get_current_user(
            required_roles=[IRoleEnum.admin, IRoleEnum.manager]
        )
    ),
) -> IPutResponseBase[IGroupRead]:
    """
    Updates a group by its id

    Required roles:
    - admin
    - manager
    """
    group_updated = await group.update(
        obj_current=current_group, obj_new=obj_in
    )
    return create_response(data=group_updated)


@router.post("/add_user/{user_id}/{group_id}")
async def add_user_into_a_group(
    user: User = Depends(user_deps.is_valid_user),
    obj_in: Group = Depends(group_deps.get_group_by_id),
    current_user: User = Depends(
        deps.get_current_user(
            required_roles=[IRoleEnum.admin, IRoleEnum.manager]
        )
    ),
) -> IPostResponseBase[IGroupRead]:
    """
    Adds a user into a group

    Required roles:
    - admin
    - manager
    """
    obj_out = await group.add_user_to_group(user=user, group_id=obj_in.id)
    return create_response(message="User added to group", data=obj_out)
