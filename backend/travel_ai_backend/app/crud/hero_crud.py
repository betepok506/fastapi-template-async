from datetime import datetime

from sqlmodel import and_, col, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from travel_ai_backend.app.crud.base_crud import CRUDBase
from travel_ai_backend.app.models.hero_model import Hero
from travel_ai_backend.app.schemas.hero_schema import IHeroCreate, IHeroUpdate


class CRUDHero(CRUDBase[Hero, IHeroCreate, IHeroUpdate]):
    async def get_heroe_by_name(
        self, *, name: str, db_session: AsyncSession | None = None
    ) -> Hero:
        db_session = db_session or super().get_db().session
        heroe = await db_session.execute(
            select(Hero).where(col(Hero.name).ilike(f"%{name}%"))
        )
        return heroe.scalars().all()

    async def get_count_of_heroes(
        self,
        *,
        start_time: datetime,
        end_time: datetime,
        db_session: AsyncSession | None = None,
    ) -> int:
        db_session = db_session or super().get_db().session
        subquery = (
            select(Hero)
            .where(
                and_(
                    Hero.created_at > start_time,
                    Hero.created_at < end_time,
                )
            )
            .subquery()
        )
        query = select(func.count()).select_from(subquery)
        count = await db_session.execute(query)
        value = count.scalar_one_or_none()
        return value


hero = CRUDHero(Hero)
