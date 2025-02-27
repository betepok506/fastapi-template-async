from pydantic import computed_field
from sqlmodel import SQLModel

from travel_ai_backend.app import api
from travel_ai_backend.app.core.config import settings
from travel_ai_backend.app.models.base_uuid_model import BaseUUIDModel
from travel_ai_backend.app.utils.minio_client import MinioClient


class MediaBase(SQLModel):
    title: str | None = None
    description: str | None = None
    path: str | None = None


class Media(BaseUUIDModel, MediaBase, table=True):
    @computed_field
    @property
    def link(self) -> str | None:
        if self.path is None:
            return ""
        minio: MinioClient = api.deps.minio_auth()
        url = minio.presigned_get_object(
            bucket_name=settings.MINIO_BUCKET, object_name=self.path
        )
        return url
