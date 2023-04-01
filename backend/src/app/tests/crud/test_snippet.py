import pytest
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas import LanguageCreate
from app.schemas.snippet import SnippetCreate, SnippetUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_snippet(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    snippet_text = random_lower_string()
    language = LanguageCreate(id=1, name="Java")
    snippet_in = SnippetCreate(title=title, snippet=snippet_text, language_id=language.id)
    user = await create_random_user(async_get_db)
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, user_id=user.id)
    assert snippet.title == title
    assert snippet.snippet == snippet_text
    assert snippet.language == language
    assert snippet.user_id == user.id


async def test_get_snippet(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    snippet_text = random_lower_string()
    language = LanguageCreate(id=1, name="Java")
    snippet_in = SnippetCreate(title=title, snippet=snippet_text, language_id=language.id)
    user = await create_random_user(async_get_db)
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, user_id=user.id)
    stored_snippet = await crud.snippet.get(db=async_get_db, id=snippet.id)
    assert stored_snippet
    assert snippet.id == stored_snippet.id
    assert snippet.title == stored_snippet.title
    assert snippet.snippet == stored_snippet.snippet
    assert snippet.language == language
    assert snippet.user_id == stored_snippet.user_id


async def test_update_snippet(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    snippet_text = random_lower_string()
    language = LanguageCreate(id=1, name="Java")
    snippet_in = SnippetCreate(title=title, snippet=snippet_text, language_id=language.id)
    user = await create_random_user(async_get_db)
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, user_id=user.id)
    snippet_text2 = random_lower_string()
    snippet_update = SnippetUpdate(snippet=snippet_text)
    snippet2 = await crud.snippet.update(db=async_get_db, db_obj=snippet, obj_in=snippet_update)
    assert snippet.id == snippet2.id
    assert snippet.title == snippet2.title
    assert snippet2.snippet == snippet_text2
    assert snippet.user_id == snippet2.user_id


async def test_delete_snippet(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    snippet_text = random_lower_string()
    language = LanguageCreate(id=1, name="Java")
    snippet_in = SnippetCreate(title=title, snippet=snippet_text, language_id=language.id)
    user = await create_random_user(async_get_db)
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, user_id=user.id)
    snippet2 = await crud.snippet.remove(db=async_get_db, id=snippet.id)
    snippet3 = await crud.snippet.get(db=async_get_db, id=snippet.id)
    assert snippet3 is None
    assert snippet2.id == snippet.id
    assert snippet2.title == title
    assert snippet2.snippet == snippet_text
    assert snippet2.user_id == user.id
