from pydantic import BaseModel


# Shared properties
class LinkBase(BaseModel):
    url: str


# Properties to receive on  link creation
class LinkCreate(LinkBase):
    url: str
    snippet_id: int


# Properties to receive on  link update
class LinkUpdate(LinkBase):
    pass


# Properties shared by models stored in DB
class LinkInDBBase(LinkBase):
    id: int
    url: str
    snippet_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Link(LinkInDBBase):
    pass


# Properties stored in DB
class LinkInDB(LinkInDBBase):
    pass
