from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, UniqueConstraint, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Enum as SqlEnum
from schemas.anime import AnimeStatusEnum

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

anime_genre_table = Table(
    "anime_genres",
    Base.metadata,
    Column("anime_id", ForeignKey("anime.mal_id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)

class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String, nullable=False, unique=True)
    display_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    anime_list = relationship("UserAnime", back_populates="user")

class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    anime = relationship("Anime", secondary=anime_genre_table, back_populates="genres")

class Anime(Base):
    __tablename__ = "anime"
    mal_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    thumbnail: Mapped[str] = mapped_column(String)
    total_episodes: Mapped[int] = mapped_column(Integer)

    genres = relationship("Genre", secondary=anime_genre_table, back_populates="anime")
    user_entries = relationship("UserAnime", back_populates="anime")

class UserAnime(Base):
    __tablename__ = "user_anime"
    __table_args__ = (UniqueConstraint("user_id", "anime_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    anime_id: Mapped[int] = mapped_column(ForeignKey("anime.mal_id"))

    status: Mapped[AnimeStatusEnum] = mapped_column(SqlEnum(AnimeStatusEnum, name="anime_status", native_enum=False))
    user_score: Mapped[int] = mapped_column(Integer, nullable=True)
    user_review: Mapped[str] = mapped_column(Text, nullable=True)
    complete_episodes: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="anime_list")
    anime = relationship("Anime", back_populates="user_entries")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)