from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Language])
async def read_languages(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve languages.
    """
    languages = await crud.language.get_multi(db, skip=skip, limit=limit)
    return languages


@router.get("/{id}", response_model=schemas.Language)
async def read_language(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        id: int,
) -> Any:
    """
    Get language by ID.
    """
    language = await crud.language.get(db=db, id=id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language
