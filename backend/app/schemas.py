import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str | None = None
    display_name: str | None = None
    description: str | None = None
    avatar_url: str | None = None

class UserCreate(schemas.BaseUserCreate):
    username: str | None = None

class UserUpdate(schemas.BaseUserUpdate):
    username: str | None = None
    display_name: str | None = None
    description: str | None = None
    avatar_url: str | None = None