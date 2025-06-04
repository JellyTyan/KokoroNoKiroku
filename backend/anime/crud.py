import httpx
from typing import List, Dict, Any
import asyncio
from datetime import datetime, timedelta

# Кэш для топ аниме с временем жизни 1 час
TOP_ANIME_CACHE: Dict[str, Dict[str, Any]] = {}
ANIME_CACHE = {}

async def fetch_top_anime(filter_param: str) -> List[Dict[str, Any]]:
    # Проверяем кэш
    cache_key = f"top_anime_{filter_param}"
    if cache_key in TOP_ANIME_CACHE:
        cache_data = TOP_ANIME_CACHE[cache_key]
        if datetime.now() - cache_data["timestamp"] < timedelta(hours=1):
            return cache_data["data"]

    # Запрашиваем 10 аниме для разнообразия
    params = {
        "type": "tv",
        "filter": filter_param,
        "sfw": "true",
        "limit": 10
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.jikan.moe/v4/top/anime", params=params)
    response.raise_for_status()
    data = response.json()["data"]

    # Фильтруем и форматируем данные
    seen_ids = set()
    filtered_list = []
    
    for anime in data:
        mal_id = anime["mal_id"]
        if mal_id not in seen_ids and len(filtered_list) < 5:  # Ограничиваем до 5 аниме
            seen_ids.add(mal_id)
            filtered_list.append({
                "mal_id": mal_id,
                "title": anime["titles"][0]["title"],
                "cover": anime["images"]["webp"]["image_url"],
                "score": anime.get("score", 0),
                "episodes": anime.get("episodes", 0),
                "status": anime.get("status", "Unknown"),
                "aired": {
                    "from": anime.get("aired", {}).get("from", None),
                    "to": anime.get("aired", {}).get("to", None)
                }
            })

    # Сохраняем в кэш
    TOP_ANIME_CACHE[cache_key] = {
        "data": filtered_list,
        "timestamp": datetime.now()
    }

    return filtered_list


async def fetch_mal(anime_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.jikan.moe/v4/anime/{anime_id}")
    r.raise_for_status()
    return r.json()["data"]


async def fetch_consument_by_name(anime_name: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"http://0.0.0.0:3000/meta/anilist/{anime_name}")
    r.raise_for_status()
    return r.json()


async def fetch_data_from_mal_and_consument(anime_id: int):
    mal_data = await fetch_mal(anime_id)
    anime_name = mal_data["title"]

    consument_data = await fetch_consument_by_name(anime_name)

    anilist_id = consument_data["results"][0]["id"]

    async with httpx.AsyncClient() as client:
        consument_anime_request = await client.get(f"http://0.0.0.0:3000/meta/anilist/info/{anilist_id}")
    consument_anime_request.raise_for_status()

    return mal_data, consument_anime_request.json()


async def fetch_anime_details(anime_id: int):
    if anime_id in ANIME_CACHE:
        return ANIME_CACHE[anime_id]

    mal_data, consument_data = await fetch_data_from_mal_and_consument(anime_id)

    anime_data = {
        "id": anime_id,
        "title": mal_data.get("title"),
        "title_english": consument_data.get("title", {}).get("english"),
        "title_japanese": consument_data.get("title", {}).get("romaji"),
        "image": mal_data.get("images", {}).get("webp", {}).get("image_url"),
        "large_image": mal_data.get("images", {}).get("webp", {}).get("large_image_url"),
        "youtube_embed": mal_data.get("trailer", {}).get("embed_url"),
        "score": mal_data.get("score"),
        "scored_by": mal_data.get("scored_by"),
        "type": mal_data.get("type"),
        "source": mal_data.get("source"),
        "episodeDuration": consument_data.get("duration"),
        "totalEpisodes": consument_data.get("totalEpisodes"),
        "currentEpisode": consument_data.get("currentEpisode"),
        "status": consument_data.get("status"),
        "releaseDate": consument_data.get("releaseDate"),
        "startDate": consument_data.get("startDate"),
        "endDate": consument_data.get("endDate"),
        "nextAiringEpisode": consument_data.get("nextAiringEpisode"),
        "rating": mal_data.get("rating"),
        "season": mal_data.get("season"),
        "year": mal_data.get("year"),
        "synopsis": consument_data.get("description"),
        "genres": [genre.get("name") for genre in mal_data.get("genres", [])],
    }

    ANIME_CACHE[anime_id] = anime_data
    return anime_data
