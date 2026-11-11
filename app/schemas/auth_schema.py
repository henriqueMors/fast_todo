from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
    exp: Optional[int] = None