from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Tag])
async def read_tags(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tags.
    """
    if crud.user.is_superuser(current_user):
        tags = await crud.tag.get_multi(db, skip=skip, limit=limit)
    else:
        tags = await crud.tag.get_multi_by_owner(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return tags


@router.post("/", response_model=schemas.Tag)
async def create_tag(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        tag_in: schemas.TagCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new tag.
    """
    tag = await crud.tag.create_with_owner(db=db, obj_in=tag_in, user_id=current_user.id)
    return tag


@router.put("/{id}", response_model=schemas.Tag)
async def update_tag(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        id: int,
        tag_in: schemas.TagUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an tag.
    """
    tag = await read_tag(db=db, id=id, current_user=current_user)
    tag = await crud.tag.update(db=db, db_obj=tag, obj_in=tag_in)
    return tag


@router.delete("/{id}", response_model=schemas.Tag)
async def delete_tag(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an tag.
    """
    tag = await read_tag(db=db, id=id, current_user=current_user)
    tag = crud.tag.remove(db=db, id=id)
    return tag


async def read_tag(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    This method is used by other methods, but isn't accessible as an API endpoint
    """
    tag = await crud.tag.get(db=db, id=id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if not crud.user.is_superuser(current_user) and (tag.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return tag
