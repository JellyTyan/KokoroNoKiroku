from fastapi import HTTPException
from typing import Any, Dict, List, Optional

class AnimeValidationError(HTTPException):
    def __init__(
        self,
        detail: str,
        errors: Optional[List[Dict[str, Any]]] = None,
        status_code: int = 422
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "message": detail,
                "errors": errors or []
            }
        )

class AnimeNotFoundError(HTTPException):
    def __init__(self, anime_id: int):
        super().__init__(
            status_code=404,
            detail=f"Anime with ID {anime_id} not found"
        )

class AnimeAlreadyInListError(HTTPException):
    def __init__(self, anime_id: int):
        super().__init__(
            status_code=400,
            detail=f"Anime with ID {anime_id} is already in your list"
        )

class InvalidAnimeStatusError(HTTPException):
    def __init__(self, status: str):
        super().__init__(
            status_code=422,
            detail=f"Invalid anime status: {status}. Must be one of: watched, planned, completed"
        ) 