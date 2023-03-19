from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .snippet import Snippet


class Language(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    snippets: "Snippet" = relationship("Snippet")
