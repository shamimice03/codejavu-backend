from typing import List

from pydantic import BaseModel

from app.models import User
from app.models.language import Language
from app.models.link import Link
from app.models.tag import Tag
from app.schemas.language import LanguageBase
from app.schemas.link import LinkBase
from app.schemas.tag import TagBase
from app.schemas.user import UserBase


# Shared properties
class SnippetBase(BaseModel):
    title: str
    snippet: str


# Properties to receive on snippet creation
class SnippetCreate(SnippetBase):
    title: str
    snippet: str
    language_id: int


# Properties to receive on snippet update
class SnippetUpdate(SnippetBase):
    pass


# Properties shared by models stored in DB
class SnippetInDBBase(SnippetBase):
    id: int
    title: str
    snippet: str
    user_id: int
    language_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Snippet(SnippetInDBBase):
    pass


# Properties stored in DB
class SnippetInDB(SnippetInDBBase):
    pass
