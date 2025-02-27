from enum import Enum
from uuid import UUID

from travel_ai_backend.app.models.role_model import RoleBase
from travel_ai_backend.app.utils.partial import optional


class IRoleCreate(RoleBase):
    pass


# All these fields are optional
@optional()
class IRoleUpdate(RoleBase):
    pass


class IRoleRead(RoleBase):
    id: UUID


class IRoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"
