from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Snippet])
async def read_snippets(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve snippets.
    """
    if crud.user.is_superuser(current_user):
        snippets = await crud.snippet.get_multi(db, skip=skip, limit=limit)
    else:
        snippets = await crud.snippet.get_multi_by_owner(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return snippets


@router.post("/", response_model=schemas.Snippet)
async def create_snippet(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        snippet_in: schemas.SnippetCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new snippet.
    """
    snippet = await crud.snippet.create_with_owner(db=db, obj_in=snippet_in, user_id=current_user.id)
    return snippet


@router.get("/{id}", response_model=schemas.Snippet)
async def read_snippet(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get snippet by ID.
    """
    snippet = await crud.snippet.get(db=db, id=id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    if not crud.user.is_superuser(current_user) and (snippet.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return snippet


@router.put("/{id}", response_model=schemas.Snippet)
async def update_snippet(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        id: int,
        snippet_in: schemas.SnippetUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an snippet.
    """
    snippet = await read_snippet(db=db, id=id, current_user=current_user)
    snippet = await crud.snippet.update(db=db, db_obj=snippet, obj_in=snippet_in)
    return snippet


@router.delete("/{id}", response_model=schemas.Snippet)
async def delete_snippet(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an snippet.
    """
    snippet = await read_snippet(db=db, id=id, current_user=current_user)
    snippet = crud.snippet.remove(db=db, id=id)
    return snippet
