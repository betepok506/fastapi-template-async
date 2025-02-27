from travel_ai_backend.app.crud.base_crud import CRUDBase
from travel_ai_backend.app.models.image_media_model import ImageMedia
from travel_ai_backend.app.schemas.image_media_schema import (
    IImageMediaCreate,
    IImageMediaUpdate,
)


class CRUDImageMedia(
    CRUDBase[ImageMedia, IImageMediaCreate, IImageMediaUpdate]
):
    pass


image = CRUDImageMedia(ImageMedia)
