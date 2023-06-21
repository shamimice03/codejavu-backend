from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    token: str
    user_id: int


class TokenPayload(BaseModel):
    sub: Optional[int] = None
