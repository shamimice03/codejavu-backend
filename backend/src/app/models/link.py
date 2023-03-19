from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base_class import Base


class Link(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    url: str = Column(String, index=True)
    snippet_id: int = Column(Integer, ForeignKey("snippet.id"))
