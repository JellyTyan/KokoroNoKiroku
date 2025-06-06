import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.db import get_async_session
from app.users import current_active_user
from database.db import Anime, Genre, User, UserAnime
from schemas.anime import AnimeCreate, AnimeUpdate, AnimeOut, AnimeStatusEnum
from app.exceptions import (
    AnimeValidationError,
    AnimeNotFoundError,
    AnimeAlreadyInListError,
    InvalidAnimeStatusError
)

router = APIRouter(tags=["Anime List"])

@router.post("/", response_model=AnimeOut)
async def add_anime(
    data: AnimeCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    try:
        # Проверяем существование аниме
        anime = await session.get(Anime, data.mal_id)
        if not anime:
            anime = Anime(
                mal_id=data.mal_id,
                title=data.title,
                thumbnail=data.thumbnail,
                total_episodes=data.total_episodes
            )
            session.add(anime)
            await session.flush()

        # Проверяем, не добавлено ли уже аниме в список пользователя
        result = await session.execute(
            select(UserAnime).where(
                UserAnime.user_id == user.id,
                UserAnime.anime_id == data.mal_id
            )
        )
        existing_entry = result.scalar_one_or_none()
        if existing_entry:
            raise AnimeAlreadyInListError(data.mal_id)

        # Создаем новую запись
        user_anime = UserAnime(
            user_id=user.id,
            anime_id=data.mal_id,
            status=data.status,
            user_score=data.user_score,
            user_review=data.user_review,
            complete_episodes=data.complete_episodes
        )
        session.add(user_anime)
        await session.commit()
        await session.refresh(user_anime)

        return AnimeOut(
            mal_id=anime.mal_id,
            title=anime.title,
            thumbnail=anime.thumbnail,
            total_episodes=anime.total_episodes,
            status=user_anime.status,
            user_score=user_anime.user_score,
            user_review=user_anime.user_review,
            complete_episodes=user_anime.complete_episodes
        )
    except AnimeAlreadyInListError:
        raise
    except Exception as e:
        logging.error(f"Error adding anime to list: {str(e)}")
        raise AnimeValidationError(
            detail="Failed to add anime to list",
            errors=[{"error": str(e)}]
        )

@router.patch("/{mal_id}", response_model=AnimeOut)
async def update_anime(
    mal_id: int,
    data: AnimeUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    try:
        # Проверяем существование записи
        result = await session.execute(
            select(UserAnime)
            .where(
                UserAnime.user_id == user.id,
                UserAnime.anime_id == mal_id
            )
            .options(selectinload(UserAnime.anime))
        )
        user_anime = result.scalar_one_or_none()
        if not user_anime:
            raise AnimeNotFoundError(mal_id)

        # Обновляем поля
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "status" and value not in AnimeStatusEnum.__members__.values():
                raise InvalidAnimeStatusError(str(value))
            setattr(user_anime, key, value)

        await session.commit()
        await session.refresh(user_anime)

        return AnimeOut(
            mal_id=user_anime.anime.mal_id,
            title=user_anime.anime.title,
            thumbnail=user_anime.anime.thumbnail,
            total_episodes=user_anime.anime.total_episodes,
            status=user_anime.status,
            user_score=user_anime.user_score,
            user_review=user_anime.user_review,
            complete_episodes=user_anime.complete_episodes
        )
    except (AnimeNotFoundError, InvalidAnimeStatusError):
        raise
    except Exception as e:
        logging.error(f"Error updating anime: {str(e)}")
        raise AnimeValidationError(
            detail="Failed to update anime",
            errors=[{"error": str(e)}]
        )

@router.delete("/{mal_id}")
async def delete_anime(
    mal_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    try:
        result = await session.execute(
            select(UserAnime).where(
                UserAnime.user_id == user.id,
                UserAnime.anime_id == mal_id
            )
        )
        user_anime = result.scalar_one_or_none()
        if not user_anime:
            raise AnimeNotFoundError(mal_id)

        await session.delete(user_anime)
        await session.commit()
        return {"detail": "Anime deleted successfully"}
    except AnimeNotFoundError:
        raise
    except Exception as e:
        logging.error(f"Error deleting anime: {str(e)}")
        raise AnimeValidationError(
            detail="Failed to delete anime",
            errors=[{"error": str(e)}]
        )

@router.get("/{status}", response_model=list[AnimeOut])
async def get_anime_by_status(
    status: AnimeStatusEnum,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    try:
        result = await session.execute(
            select(UserAnime)
            .where(
                UserAnime.user_id == user.id,
                UserAnime.status == status
            )
            .options(selectinload(UserAnime.anime))
        )
        entries = result.scalars().all()

        return [
            AnimeOut(
                mal_id=e.anime.mal_id,
                title=e.anime.title,
                thumbnail=e.anime.thumbnail,
                total_episodes=e.anime.total_episodes,
                status=e.status,
                user_score=e.user_score,
                user_review=e.user_review,
                complete_episodes=e.complete_episodes
            )
            for e in entries
        ]
    except Exception as e:
        logging.error(f"Error getting anime by status: {str(e)}")
        raise AnimeValidationError(
            detail="Failed to get anime list",
            errors=[{"error": str(e)}]
        )