from fastapi_users.manager import BaseUserManager
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends
from .models import User
from backend.database.db import get_user_db  # ты уже это сделал

SECRET = "SUPER_SECRET_KEY"  # замени на свой

class UserManager(BaseUserManager[User, int]):
    user_db_model = User
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    # необязательно, но можно переопределить методы
    async def on_after_register(self, user: User, request=None):
        print(f"User {user.id} has registered.")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
