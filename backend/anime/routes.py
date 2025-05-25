from fastapi import APIRouter, HTTPException, Query
from typing import List

from backend.anime.crud import (
    fetch_top_anime,
    fetch_anime_details,
)

router = APIRouter()


@router.get("/top-anime")
async def get_top_anime(filter: str = Query("bypopularity")) -> List[dict]:
    """
    Получить топ аниме с фильтром.
    """
    try:
        anime_list = await fetch_top_anime(filter)
        return anime_list
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch data from the API")


@router.get("/anime/{anime_id}")
async def get_anime(anime_id: int):
    """
    Получить подробности аниме по ID
    """
    try:
        anime_data = await fetch_anime_details(anime_id)
        if not anime_data:
            raise HTTPException(status_code=404, detail="Anime not found")
        return anime_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
