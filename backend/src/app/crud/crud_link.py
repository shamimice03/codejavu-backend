from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.crud.base import CRUDBase
from app.models.link import Link
from app.schemas.link import LinkCreate, LinkUpdate


class CRUDLink(CRUDBase[Link, LinkCreate, LinkUpdate]):
    async def create_with_owner(
            self, db: AsyncSession, *, obj_in: LinkCreate, user_id: int
    ) -> Link:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
            self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Link]:
        result = await db.execute(
            select(self.model)
            .filter(Link.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return list(result.scalars().all())


link = CRUDLink(Link)
