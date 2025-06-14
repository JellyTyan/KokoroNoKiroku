from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI

from database.db import User, create_db_and_tables
from .schemas import UserCreate, UserRead, UserUpdate
from .users import (auth_backend, current_active_user, fastapi_users)
from anime.routes import router as anime_router
from api.anime_list import router as anime_list_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/api/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/users",
    tags=["users"],
)

app.include_router(anime_router, prefix="/api")

app.include_router(anime_list_router, prefix="/api/anime-list", tags=["Anime List"])


@app.get("/me")
async def get_profile(user: User = Depends(current_active_user)):
    return user

@app.post("/me/update")
async def update_profile(username: str, user: User = Depends(current_active_user)):
    user.username = username
    # DB update here :3
    return {"status": "updated"}