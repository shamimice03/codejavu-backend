from typing import Optional

#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.schemas.snippet import SnippetCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_snippet(db: AsyncSession, *, user_id: Optional[int] = None) -> models.Snippet:
    if user_id is None:
        user = await create_random_user(db)
        user_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    snippet_in = SnippetCreate(title=title, description=description, id=id)
    return await crud.snippet.create_with_owner(db=db, obj_in=snippet_in, user_id=user_id)
