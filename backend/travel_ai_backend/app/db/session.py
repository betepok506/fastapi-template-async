# https://stackoverflow.com/questions/75252097/fastapi-testing-runtimeerror-task-attached-to-a-different-loop/75444607#75444607
from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import RequestError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool
from sqlmodel.ext.asyncio.session import AsyncSession

from travel_ai_backend.app.core.config import ModeEnum, settings

DB_POOL_SIZE = 83
WEB_CONCURRENCY = 9
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

connect_args = {"check_same_thread": False}

engine = create_async_engine(
    str(settings.ASYNC_DATABASE_URI),
    echo=False,
    poolclass=(
        NullPool
        if settings.MODE == ModeEnum.testing
        else AsyncAdaptedQueuePool
    ),  # Asincio pytest works with NullPool
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

engine_celery = create_async_engine(
    str(settings.ASYNC_CELERY_BEAT_DATABASE_URI),
    echo=False,
    poolclass=(
        NullPool
        if settings.MODE == ModeEnum.testing
        else AsyncAdaptedQueuePool
    ),  # Asincio pytest works with NullPool
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

SessionLocalCelery = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_celery,
    class_=AsyncSession,
    expire_on_commit=False,
)


class ElasticSearchSession:
    def __init__(self, hosts: List[str]):
        self.es = AsyncElasticsearch(hosts=hosts)

    async def __aenter__(self):
        return self.es

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.es.close()


SessionLocalElasticSearch = ElasticSearchSession(
    hosts=[settings.ELASTIC_SEARCH_DATABASE_URI]
)
