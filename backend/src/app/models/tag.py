from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base_class import Base


class Tag(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    url: str = Column(String, index=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
