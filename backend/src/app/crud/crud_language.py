from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.crud.base import CRUDBase
from app.models.language import Language
from app.schemas.language import LanguageCreate, LanguageUpdate


class CRUDLanguage(CRUDBase[Language, LanguageCreate, LanguageUpdate]):
    async def create(
            self, db: AsyncSession, *, obj_in: LanguageCreate
    ) -> Language:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Language]:
        result = await db.execute(
            select(self.model)
            .all()
        )
        return list(result.scalars().all())


language = CRUDLanguage(Language)
