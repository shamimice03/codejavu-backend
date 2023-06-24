#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = await crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = await crud.user.create(db, obj_in=user_in)  # noqa: F841
        user = await crud.user.update(db, db_obj=user, obj_in={"is_active": True})  # noqa: F841

    languages = [
        {"id": 1, "name": "Java"},
        {"id": 2, "name": "Python"},
    ]
    for language in languages:
        language_in = schemas.LanguageCreate(id=language["id"], name=language["name"])
        if not language_in:
            language = await crud.language.create(db, obj_in=language_in)  # noqa: F841

