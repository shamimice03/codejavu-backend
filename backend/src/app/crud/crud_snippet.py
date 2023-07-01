import logging
from typing import List, Dict, Any, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app import crud
from app.crud.base import CRUDBase
from app.models import Link, Tag
from app.models.snippet import Snippet
from app.schemas.link import LinkBase
from app.schemas.snippet import SnippetCreate, SnippetUpdate


class CRUDSnippet(CRUDBase[Snippet, SnippetCreate, SnippetUpdate]):
    async def create_with_owner(
            self, db: AsyncSession, *, obj_in: SnippetCreate, user_id: int
    ) -> Snippet:
        db_obj = self.model(
            title=obj_in.dict().get("title"),  # type: ignore
            snippet=obj_in.dict().get("snippet"),  # type: ignore
            language_id=obj_in.dict().get("language_id"),  # type: ignore
            user_id=user_id)  # type: ignore

        tag_ids = obj_in.dict().get("tag_ids")
        if tag_ids:
            tags = await self.create_tag_list_from_ids(db, tag_ids)
            db_obj.tags.extend(tags)

        db.add(db_obj)

        await db.flush()  # flushing to get id
        link_list = obj_in.dict().get("links")
        if link_list:
            db = await self.add_links_to_db(db, db_obj.id, link_list)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
            self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Snippet]:
        result = await db.execute(
            select(self.model)
            .filter(Snippet.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return list(result.scalars().all())

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: Snippet,
            obj_in: Union[SnippetUpdate, Dict[str, Any]]
    ) -> Snippet:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data.pop('links', None)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db_obj.tags.clear()
        tag_ids = obj_in.dict().get("tag_ids")
        if tag_ids:
            tags = await self.create_tag_list_from_ids(db, tag_ids)
            db_obj.tags.extend(tags)

        links_to_be_deleted = await db.execute(
            select(Link)
            .filter(Link.snippet_id == db_obj.id)
        )
        links_to_delete = links_to_be_deleted.scalars().all()
        for link in links_to_delete:
            await db.delete(link)

        link_list = obj_in.dict().get("links")
        if link_list:
            db = await self.add_links_to_db(db, db_obj.id, link_list)

        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def create_tag_list_from_ids(self, db: AsyncSession, tag_ids: List[int]) -> List[Tag]:
        # Retrieve the tags from the database using the provided tag IDs
        tags = await crud.tag.get_multi_by_ids(db=db, tag_ids=tag_ids)

        if len(tags) != len(tag_ids):
            raise HTTPException(status_code=400, detail='One or more provided tag IDs are invalid')

        return tags

    async def add_links_to_db(self, db: AsyncSession, snippet_id: int, link_list: List[LinkBase]) -> AsyncSession:
        for link_data in link_list:
            link = Link(snippet_id=snippet_id, url=link_data["url"])  # type: ignore
            db.add(link)
        return db


snippet = CRUDSnippet(Snippet)
