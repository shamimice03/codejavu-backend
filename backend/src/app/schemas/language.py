from typing import Optional
from pydantic import BaseModel


# Shared properties
class LanguageBase(BaseModel):
    id: Optional[int] = None


# Properties to receive on  language creation
class LanguageCreate(LanguageBase):
    name: str


# Properties to receive on  language update
class LanguageUpdate(LanguageBase):
    pass


# Properties shared by models stored in DB
class LanguageInDBBase(LanguageBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class Language(LanguageInDBBase):
    pass


# Properties stored in DB
class LanguageInDB(LanguageInDBBase):
    pass
