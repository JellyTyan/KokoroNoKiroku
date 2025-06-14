import uuid
from typing import Optional

from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import User, get_user_db

SECRET = "SECRET"

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def authenticate(
        self, credentials: models.UP
    ) -> Optional[User]:
        user = await self.user_db.get_by_email(credentials.username.lower())
        if user is None:
            # Try to find user by username
            async with self.user_db.session as session:
                stmt = select(User).where(User.username == credentials.username.lower())
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()

        if user is None:
            return None
        if not user.is_active:
            return None
        if not self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )[0]:
            return None
        return user

    async def create(
        self,
        user_create,
        safe: bool = False,
        request=None,
    ) -> User:
        try:
            return await super().create(user_create, safe=safe, request=request)
        except UserAlreadyExists:
            raise HTTPException(
                status_code=409,
                detail="User exists"
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport(
    cookie_name="access_token",  
    cookie_max_age=3600,
    cookie_secure=False,         
    cookie_httponly=True,
)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret="SECRET", lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)