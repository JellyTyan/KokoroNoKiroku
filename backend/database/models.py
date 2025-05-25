from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.db import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
