from pydantic import BaseModel
from typing import Optional
from enum import Enum

class AnimeStatusEnum(str, Enum):
    WATCHED = "watched"
    PLANNED = "planned"
    COMPLETED = "completed"

class AnimeCreate(BaseModel):
    mal_id: int
    title: str
    thumbnail: str
    total_episodes: int
    status: AnimeStatusEnum
    user_score: Optional[int] = None
    user_review: Optional[str] = None
    complete_episodes: int = 0

class AnimeUpdate(BaseModel):
    status: Optional[AnimeStatusEnum] = None
    user_score: Optional[int] = None
    user_review: Optional[str] = None
    complete_episodes: Optional[int] = None

class AnimeOut(BaseModel):
    mal_id: int
    title: str
    thumbnail: str
    total_episodes: int
    status: AnimeStatusEnum
    user_score: Optional[int]
    user_review: Optional[str]
    complete_episodes: int

    class Config:
        from_attributes = True