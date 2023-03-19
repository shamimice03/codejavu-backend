from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .language import Language
    from .link import Link
    from .tag_assign import TagAssign


class Snippet(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    snippet: str = Column(String, index=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    user: "User" = relationship("User", back_populates="snippets")
    language_id: int = Column(Integer, ForeignKey("language.id"))
    language: "Language" = relationship("Language", back_populates="snippet")
    links: List["Link"] = relationship("Link")
    tags: List["TagAssign"] = relationship("TagAssign")
