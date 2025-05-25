from fastapi_users.db import SQLAlchemyUserDatabase
from backend.database.models import User
from backend.database.db import SessionLocal

async def get_user_db():
    async with SessionLocal() as session:
        yield SQLAlchemyUserDatabase(session, User)
