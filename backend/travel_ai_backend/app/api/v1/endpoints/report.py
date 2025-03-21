from enum import Enum
from io import BytesIO, StringIO
from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from travel_ai_backend.app.crud.hero_crud import hero
from travel_ai_backend.app.crud.user_crud import user
from travel_ai_backend.app.api import deps
from travel_ai_backend.app.models.user_model import User
from travel_ai_backend.app.schemas.hero_schema import IHeroRead
from travel_ai_backend.app.schemas.role_schema import IRoleEnum

# from travel_ai_backend.app.schemas.user_schema import IUserRead
from travel_ai_backend.app.schemas.user_schema import IUserRead

router = APIRouter()


class FileExtensionEnum(str, Enum):
    csv = "csv"
    xls = "xls"


@router.get("/users_list")
async def export_users_list(
    file_extension: Annotated[
        FileExtensionEnum,
        Query(
            description="This is the exported file format",
        ),
    ] = FileExtensionEnum.csv,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> StreamingResponse:
    """
    Export users list in a csv/xlsx file

    Required roles:
    - admin
    """
    users = await user.get_multi_ordered(limit=1000, order_by="id")
    users_list = [
        IUserRead.model_validate(cur_user) for cur_user in users
    ]  # Creates a pydantic list of object
    users_df = pd.DataFrame([s.__dict__ for s in users_list])
    if file_extension == FileExtensionEnum.xls:
        stream = BytesIO()
        with pd.ExcelWriter(stream) as writer:
            users_df.to_excel(writer, index=False)
        media_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        filename = "users.xlsx"
    else:
        stream = StringIO()
        users_df.to_csv(stream, index=False)
        media_type = "text/csv"
        filename = "users.csv"

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment;filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )

    return response


@router.get("/heroes_list")
async def export_heroes_list(
    file_extension: FileExtensionEnum = Query(
        default=FileExtensionEnum.csv,
        description="This is the exported file format",
    ),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> StreamingResponse:
    """
    Export heroes list in a csv/xlsx file

    Required roles:
    - admin
    """
    heroes = await hero.get_multi_ordered(limit=1000, order_by="id")
    heroes_list = [
        IHeroRead.model_validate(cur_hero) for cur_hero in heroes
    ]  # Creates a pydantic list of object
    heroes_df = pd.DataFrame([s.__dict__ for s in heroes_list])
    if file_extension == FileExtensionEnum.xls:
        stream = BytesIO()
        with pd.ExcelWriter(stream) as writer:
            heroes_df.to_excel(writer, index=False)
        media_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        filename = "heroes.xlsx"
    else:
        stream = StringIO()
        heroes_df.to_csv(stream, index=False)
        media_type = "text/csv"
        filename = "heroes.csv"

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment;filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )

    return response
