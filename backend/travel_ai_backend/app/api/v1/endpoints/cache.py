from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from travel_ai_backend.app.crud.hero_crud import hero
from travel_ai_backend.app.schemas.response_schema import (
    IGetResponseBase,
    create_response,
)

router = APIRouter()


@router.get("/cached")
@cache(expire=10)
async def get_a_cached_response() -> IGetResponseBase[str | datetime]:
    """
    Gets a cached datetime
    """
    return create_response(data=datetime.now())


@router.get("/no_cached")
async def get_a_normal_response() -> IGetResponseBase[str | datetime]:
    """
    Gets a real-time datetime
    """
    return create_response(data=datetime.now())


@router.get("/heroe_count/cached")
@cache(expire=20)
async def get_count_of_heroes_created_cached(
    start_date: Annotated[date, Query(title="start date for get data")] = (
        datetime.now() - timedelta(days=7)
    ).date(),
    end_date: Annotated[
        date, Query(title="end date for get data")
    ] = datetime.now().date(),
) -> IGetResponseBase[int]:
    """
    Gets count of heroes created on a base time (Cached response)
    """
    count = await hero.get_count_of_heroes(
        start_time=datetime.combine(start_date, datetime.min.time()),
        end_time=datetime.combine(end_date, datetime.min.time()),
    )
    return create_response(message="message", data=count)


@router.get("/heroe_count/no_cached")
async def get_count_of_heroes_created_no_cached(
    start_date: Annotated[date, Query(title="start date for get data")] = (
        datetime.now() - timedelta(days=7)
    ).date(),
    end_date: Annotated[
        date, Query(title="end date for get data")
    ] = datetime.now().date(),
) -> IGetResponseBase[int]:
    """
    Gets count of heroes created on a base time (No Cached response)
    """
    count = await hero.get_count_of_heroes(
        start_time=datetime.combine(start_date, datetime.min.time()),
        end_time=datetime.combine(end_date, datetime.min.time()),
    )
    return create_response(message="", data=count)
