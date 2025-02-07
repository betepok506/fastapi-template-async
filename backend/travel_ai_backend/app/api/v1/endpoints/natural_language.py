from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import sqlalchemy
import sqlmodel

from travel_ai_backend.app import crud
from travel_ai_backend.app.api import deps
from travel_ai_backend.app.api.deps import get_redis_client
from travel_ai_backend.app.core import security
from travel_ai_backend.app.core.config import settings
from travel_ai_backend.app.core.security import decode_token, get_password_hash, verify_password
from travel_ai_backend.app.models.user_model import User
from travel_ai_backend.app.schemas.common_schema import IMetaGeneral, TokenType
from travel_ai_backend.app.schemas.response_schema import IPostResponseBase, create_response
from travel_ai_backend.app.schemas.token_schema import RefreshToken, Token, TokenRead
from travel_ai_backend.app.utils.token import add_token_to_redis, delete_tokens, get_valid_tokens

from travel_ai_backend.app.api import deps
from travel_ai_backend.app.api.celery_task import predict_transformers_pipeline
from travel_ai_backend.app.models.user_model import User
from travel_ai_backend.app.utils.fastapi_globals import g
from travel_ai_backend.app.schemas.response_schema import IPostResponseBase, create_response
from travel_ai_backend.app.core.celery import celery

router = APIRouter()


@router.post(
    "/sentiment_analysis",
    dependencies=[
        Depends(RateLimiter(times=10, hours=24)),
    ],
)
async def sentiment_analysis_prediction(
    prompt: str = "Fastapi is awesome",
    current_user: User = Depends(deps.get_current_user()),
) -> IPostResponseBase:
    """
    Gets a sentimental analysis predition using a NLP model from transformers libray
    """
    sentiment_model = g.sentiment_model
    prediction = sentiment_model(prompt)
    return create_response(message="Prediction got succesfully", data=prediction)


@router.post(
    "/text_generation_prediction_batch_task",
    dependencies=[
        Depends(RateLimiter(times=10, hours=24)),
    ],
)
async def text_generation_prediction_batch_task(
    prompt: str = "Batman is awesome because",
) -> IPostResponseBase:
    """
    Async batch task for text generation using a NLP model from transformers libray
    """
    prection_task = predict_transformers_pipeline.delay(prompt)
    return create_response(
        message="Prediction got succesfully", data={"task_id": prection_task.task_id}
    )


@router.post(
    "/text_generation_prediction_batch_task_after_some_seconds",
    dependencies=[
        Depends(RateLimiter(times=10, hours=24)),
    ],
)
async def text_generation_prediction_batch_task_after_some_seconds(
    prompt: str = "Batman is awesome because", seconds: float = 5
) -> IPostResponseBase:
    """
    Async batch task for text generation using a NLP model from transformers libray

    It is executed after x number of seconds
    """
    delay_elapsed = datetime.utcnow() + timedelta(seconds=seconds)
    prection_task = predict_transformers_pipeline.apply_async(
        args=[prompt], eta=delay_elapsed
    )
    return create_response(
        message="Prediction got succesfully", data={"task_id": prection_task.task_id}
    )


@router.get(
    "/get_result_from_batch_task",
    dependencies=[
        Depends(RateLimiter(times=10, minutes=1)),
    ],
)
async def get_result_from_batch_task(task_id: str) -> IPostResponseBase:
    """
    Get result from batch task using task_id
    """
    async_result = celery.AsyncResult(task_id)
    if async_result.ready():
        print(f'Ready!!')
        if not async_result.successful():
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} with state {async_result.state}.",
            )

        result = async_result.get(timeout=1.0)
        return create_response(
            message="Prediction got succesfully",
            data={"task_id": task_id, "result": result},
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} does not exist or is still running.",
        )
