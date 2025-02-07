from travel_ai_backend.app.models.hero_model import HeroBase
from travel_ai_backend.app.models.team_model import TeamBase
from .user_schema import IUserBasicInfo
from travel_ai_backend.app.utils.partial import optional
from uuid import UUID


class ITeamCreate(TeamBase):
    pass


# All these fields are optional
@optional()
class ITeamUpdate(TeamBase):
    pass


class ITeamRead(TeamBase):
    id: UUID
    created_by: IUserBasicInfo


class ITeamReadWithHeroes(ITeamRead):
    heroes: list[HeroBase]
