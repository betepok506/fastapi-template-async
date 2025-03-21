from collections.abc import AsyncGenerator
from typing import Callable

import redis.asyncio as aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, MissingRequiredClaimError
from prometheus_client import Counter, Histogram
from redis.asyncio import Redis
from sqlmodel.ext.asyncio.session import AsyncSession

from travel_ai_backend.app.crud.role_crud import role
from travel_ai_backend.app.crud.user_crud import user
from travel_ai_backend.app.core.config import settings
from travel_ai_backend.app.core.security import decode_token
from travel_ai_backend.app.db.session import (  # , ElasticSearchSession
    SessionLocal,
    SessionLocalCelery,
    SessionLocalElasticSearch,
)
from travel_ai_backend.app.models.user_model import User
from travel_ai_backend.app.schemas.common_schema import IMetaGeneral, TokenType
from travel_ai_backend.app.utils.minio_client import MinioClient
from travel_ai_backend.app.utils.token import get_valid_tokens

request_count = Counter("http_requests_total", "Total number of requests")
request_latency = Histogram(
    "http_request_duration_seconds", "Request latency in seconds"
)
http_404_counter = Counter(
    "http_404_errors_total", "Total number of 404 errors"
)
http_502_counter = Counter(
    "http_502_errors_total", "Total number of 502 errors"
)
http_500_counter = Counter(
    "http_500_errors_total", "Total number of 500 errors"
)
http_200_counter = Counter(
    "http_200_errors_total", "Total number of 200 response"
)


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_redis_client() -> Redis:
    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis


class ElasticsearchClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AsyncElasticsearch(
                hosts=[settings.ELASTIC_SEARCH_DATABASE_URI]
            )
        return cls._instance


async def get_elasticsearch_client():
    return ElasticsearchClient.get_instance()


# async def get_elastic_client():
#     return AsyncElasticsearch(hosts=[settings.ELASTIC_SEARCH_DATABASE_URI])
#     # async with SessionLocalElasticSearch() as es:
#     #     yield es


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_jobs_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocalCelery() as session:
        yield session


async def get_general_meta() -> IMetaGeneral:
    current_roles = await role.get_multi(skip=0, limit=100)
    return IMetaGeneral(roles=current_roles)


def get_current_user(required_roles: list[str] = None) -> Callable[[], User]:
    async def current_user(
        access_token: str = Depends(reusable_oauth2),
        redis_client: Redis = Depends(get_redis_client),
    ) -> User:
        try:
            payload = decode_token(access_token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your token has expired. Please log in again.",
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Error when decoding the token. Please check your request.",
            )
        except MissingRequiredClaimError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="There is no required field in your token. Please contact the administrator.",
            )

        user_id = payload["sub"]
        valid_access_tokens = await get_valid_tokens(
            redis_client, user_id, TokenType.ACCESS
        )
        if valid_access_tokens and access_token not in valid_access_tokens:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user_obj: User = await user.get(id=user_id)
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")

        if not user_obj.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == user_obj.role.name:
                    is_valid_role = True

            if not is_valid_role:
                raise HTTPException(
                    status_code=403,
                    detail=f"""Role "{required_roles}" is required for this action""",
                )

        return user_obj

    return current_user


def minio_auth() -> MinioClient:
    minio_client = MinioClient(
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        bucket_name=settings.MINIO_BUCKET,
        minio_url=settings.MINIO_URL,
    )
    return minio_client
