from typing import List

from pydantic import BaseModel

from app.schemas.language import Language
from app.schemas.tag import Tag


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


class SnippetWithRelatedData(Snippet):
    tags: List[Tag] = []
    language: Language = None


# Properties stored in DB
class SnippetInDB(SnippetInDBBase):
    pass
