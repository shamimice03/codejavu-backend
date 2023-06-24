from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.crud.base import CRUDBase
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    async def create_with_owner(
            self, db: AsyncSession, *, obj_in: TagCreate, user_id: int
    ) -> Tag:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
            self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Tag]:
        result = await db.execute(
            select(self.model)
            .filter(Tag.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return list(result.scalars().all())


tag = CRUDTag(Tag)
