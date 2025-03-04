from uuid import UUID

from fastapi import HTTPException, Path, status
from typing_extensions import Annotated

from travel_ai_backend.app.crud.user_crud import user
from travel_ai_backend.app.models.role_model import Role
from travel_ai_backend.app.models.user_model import User
from travel_ai_backend.app.schemas.user_schema import IUserCreate, IUserRead
from travel_ai_backend.app.utils.exceptions.common_exception import (
    IdNotFoundException,
)


async def user_exists(new_user: IUserCreate) -> IUserCreate:
    obj_user = await user.get_by_email(email=new_user.email)
    if obj_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a user with same email",
        )
    role = await role.get(id=new_user.role_id)
    if not role:
        raise IdNotFoundException(Role, id=new_user.role_id)

    return new_user


async def is_valid_user(
    user_id: Annotated[UUID, Path(title="The UUID id of the user")]
) -> IUserRead:
    obj_user = await user.get(id=user_id)
    if not obj_user:
        raise IdNotFoundException(User, id=user_id)

    return obj_user


async def is_valid_user_id(
    user_id: Annotated[UUID, Path(title="The UUID id of the user")]
) -> IUserRead:
    obj_user = await user.get(id=user_id)
    if not obj_user:
        raise IdNotFoundException(User, id=user_id)

    return user_id
