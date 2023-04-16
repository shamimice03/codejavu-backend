import logging
from typing import List

from fastapi.encoders import jsonable_encoder
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.crud.base import CRUDBase
from app.models.snippet import Snippet
from app.schemas.snippet import SnippetCreate, SnippetUpdate


class CRUDSnippet(CRUDBase[Snippet, SnippetCreate, SnippetUpdate]):
    async def create_with_owner(
            self, db: AsyncSession, *, obj_in: SnippetCreate, user_id: int
    ) -> Snippet:
        obj_in_data = jsonable_encoder(obj_in)

        db_obj = self.model(**obj_in_data, user_id=user_id)  # type: ignore

        db.add(db_obj)
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


snippet = CRUDSnippet(Snippet)
