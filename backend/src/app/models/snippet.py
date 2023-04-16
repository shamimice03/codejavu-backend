from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .tag_assign import TagAssign

if TYPE_CHECKING:
    from .user import User
    from .language import Language
    from .link import Link
    from .tag import Tag


class Snippet(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    snippet: str = Column(String, index=True)
    user_id: Column["Integer"] = Column(Integer, ForeignKey("user.id"))
    user: "User" = relationship("User", back_populates="snippets")
    language_id: int = Column(Integer, ForeignKey("language.id"))
    language: "Language" = relationship("Language", back_populates="snippets")
    links: List["Link"] = relationship("Link")
    tags: List["Tag"] = relationship("Tag", secondary=TagAssign)
