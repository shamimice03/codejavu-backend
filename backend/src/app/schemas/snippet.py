from typing import Optional

from pydantic import BaseModel


# Shared properties
class SnippetBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on snippet creation
class SnippetCreate(SnippetBase):
    title: str


# Properties to receive on snippet update
class SnippetUpdate(SnippetBase):
    pass


# Properties shared by models stored in DB
class SnippetInDBBase(SnippetBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Snippet(SnippetInDBBase):
    pass


# Properties stored in DB
class SnippetInDB(SnippetInDBBase):
    pass
