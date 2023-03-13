import pytest
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas.snippet import SnippetCreate, SnippetUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_snippet(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    snippet_in = SnippetCreate(title=title, description=description)
    user = await create_random_user(async_get_db)
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, owner_id=user.id)
    assert snippet.title == title
    assert snippet.description == description
    assert snippet.owner_id == user.id


async def test_get_snippet(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    snippet_in = SnippetCreate(title=title, description=description)
    user = await create_random_user(async_get_db)
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, owner_id=user.id)
    stored_snippet = await crud.snippet.get(db=async_get_db, id=snippet.id)
    assert stored_snippet
    assert snippet.id == stored_snippet.id
    assert snippet.title == stored_snippet.title
    assert snippet.description == stored_snippet.description
    assert snippet.owner_id == stored_snippet.owner_id


async def test_update_snippet(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    snippet_in = SnippetCreate(title=title, description=description)
    user = await create_random_user(async_get_db)
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, owner_id=user.id)
    description2 = random_lower_string()
    snippet_update = SnippetUpdate(description=description2)
    snippet2 = await crud.snippet.update(db=async_get_db, db_obj=snippet, obj_in=snippet_update)
    assert snippet.id == snippet2.id
    assert snippet.title == snippet2.title
    assert snippet2.description == description2
    assert snippet.owner_id == snippet2.owner_id


async def test_delete_snippet(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    snippet_in = SnippetCreate(title=title, description=description)
    user = await create_random_user(async_get_db)
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, owner_id=user.id)
    snippet2 = await crud.snippet.remove(db=async_get_db, id=snippet.id)
    snippet3 = await crud.snippet.get(db=async_get_db, id=snippet.id)
    assert snippet3 is None
    assert snippet2.id == snippet.id
    assert snippet2.title == title
    assert snippet2.description == description
    assert snippet2.owner_id == user.id
