from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .tag import Tag


class TagAssign(Base):
    __tablename__ = "tag_assign"
    snippet_id: int = Column("snippet_id", ForeignKey("snippet.id"), primary_key=True)
    tag_id: int = Column("tag_id", ForeignKey("tag.id"), primary_key=True)
    user_id: int = Column("user_id", ForeignKey("user.id"))
    tag: "Tag" = relationship("TagAssign")
