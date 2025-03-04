from sqlmodel.ext.asyncio.session import AsyncSession

from travel_ai_backend.app.crud.group_crud import group
from travel_ai_backend.app.crud.user_crud import user
from travel_ai_backend.app.crud.role_crud import role
from travel_ai_backend.app.crud.team_crud import team
from travel_ai_backend.app.crud.hero_crud import hero
from travel_ai_backend.app.core.config import settings
from travel_ai_backend.app.schemas.group_schema import IGroupCreate
from travel_ai_backend.app.schemas.hero_schema import IHeroCreate
from travel_ai_backend.app.schemas.role_schema import IRoleCreate
from travel_ai_backend.app.schemas.team_schema import ITeamCreate
from travel_ai_backend.app.schemas.user_schema import IUserCreate

roles: list[IRoleCreate] = [
    IRoleCreate(name="admin", description="This the Admin role"),
    IRoleCreate(name="manager", description="Manager role"),
    IRoleCreate(name="user", description="User role"),
]

groups: list[IGroupCreate] = [
    IGroupCreate(name="GR1", description="This is the first group")
]

users: list[dict[str, str | IUserCreate]] = [
    {
        "data": IUserCreate(
            first_name="Admin",
            last_name="FastAPI",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
            is_superuser=True,
        ),
        "role": "admin",
    },
    {
        "data": IUserCreate(
            first_name="Manager",
            last_name="FastAPI",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email="manager@example.com",
            is_superuser=False,
        ),
        "role": "manager",
    },
    {
        "data": IUserCreate(
            first_name="User",
            last_name="FastAPI",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email="user@example.com",
            is_superuser=False,
        ),
        "role": "user",
    },
]

teams: list[ITeamCreate] = [
    ITeamCreate(name="Preventers", headquarters="Sharp Tower"),
    ITeamCreate(name="Z-Force", headquarters="Sister Margaret's Bar"),
]

heroes: list[dict[str, str | IHeroCreate]] = [
    {
        "data": IHeroCreate(
            name="Deadpond", secret_name="Dive Wilson", age=21
        ),
        "team": "Z-Force",
    },
    {
        "data": IHeroCreate(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48
        ),
        "team": "Preventers",
    },
]


async def init_db(db_session: AsyncSession) -> None:
    for cur_role in roles:
        role_current = await role.get_role_by_name(
            name=cur_role.name, db_session=db_session
        )
        if not role_current:
            await role.create(obj_in=cur_role, db_session=db_session)

    for cur_user in users:
        current_user = await user.get_by_email(
            email=cur_user["data"].email, db_session=db_session
        )
        cur_role = await role.get_role_by_name(
            name=cur_user["role"], db_session=db_session
        )
        if not current_user:
            cur_user["data"].role_id = cur_role.id
            await user.create_with_role(
                obj_in=cur_user["data"], db_session=db_session
            )

    for cur_group in groups:
        current_group = await group.get_group_by_name(
            name=cur_group.name, db_session=db_session
        )
        if not current_group:
            current_user = await user.get_by_email(
                email=users[0]["data"].email, db_session=db_session
            )
            new_group = await group.create(
                obj_in=cur_group,
                created_by_id=current_user.id,
                db_session=db_session,
            )
            current_users = []
            for cur_user in users:
                current_users.append(
                    await user.get_by_email(
                        email=cur_user["data"].email, db_session=db_session
                    )
                )
            await group.add_users_to_group(
                users=current_users,
                group_id=new_group.id,
                db_session=db_session,
            )

    for cur_team in teams:
        current_team = await team.get_team_by_name(
            name=cur_team.name, db_session=db_session
        )
        if not current_team:
            current_user = await user.get_by_email(
                email=users[0]["data"].email, db_session=db_session
            )
            await team.create(
                obj_in=cur_team,
                created_by_id=current_user.id,
                db_session=db_session,
            )

    for heroe in heroes:
        current_heroe = await hero.get_heroe_by_name(
            name=heroe["data"].name, db_session=db_session
        )
        cur_team = await team.get_team_by_name(
            name=heroe["team"], db_session=db_session
        )
        if not current_heroe:
            current_user = await user.get_by_email(
                email=users[0]["data"].email, db_session=db_session
            )
            new_heroe = heroe["data"]
            new_heroe.team_id = cur_team.id
            await hero.create(
                obj_in=new_heroe,
                created_by_id=current_user.id,
                db_session=db_session,
            )
