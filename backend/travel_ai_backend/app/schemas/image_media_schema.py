from pydantic import model_validator

from travel_ai_backend.app.models.image_media_model import (
    ImageMedia,
    ImageMediaBase,
)
from travel_ai_backend.app.models.media_model import Media
from travel_ai_backend.app.utils.partial import optional

from .media_schema import IMediaRead


# Image Media
class IImageMediaCreate(ImageMediaBase):
    pass


# All these fields are optional
@optional()
class IImageMediaUpdate(ImageMediaBase):
    pass


class IImageMediaRead(ImageMediaBase):
    media: IMediaRead | None


# Todo make it compatible with pydantic v2
class IImageMediaReadCombined(ImageMediaBase):
    link: str | None

    @model_validator(mode="before")
    def combine_attributes(cls, values):
        link_fields = {"link": values.get("link", None)}
        if "media" in values:
            if (
                isinstance(values["media"], Media)
                and values["media"].path is not None
            ):
                link_fields = {"link": values["media"].link}

        image_media_fields = {
            k: v for k, v in values.items() if k in ImageMedia.__fields__
        }
        output = {**image_media_fields, **link_fields}
        return output
