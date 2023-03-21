from typing import Optional

from pydantic import BaseModel


# Shared properties
class TagBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


# Properties to receive on  tag creation
class TagCreate(TagBase):
    name: str
    user_id: Optional[int] = None


# Properties to receive on  tag update
class TagUpdate(TagBase):
    pass


# Properties shared by models stored in DB
class TagInDBBase(TagBase):
    id: int
    name: str
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Tag(TagInDBBase):
    pass


# Properties stored in DB
class TagInDB(TagInDBBase):
    pass
