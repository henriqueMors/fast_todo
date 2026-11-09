from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserAuth(BaseModel):
    """O que a API RECEBE no cadastro."""
    email: EmailStr = Field(..., description="E-mail do usuário")
    username: str = Field(..., min_length=5, max_length=50, description="Nome de usuário")
    password: str = Field(..., min_length=5, max_length=24, description="Senha do usuário")


class UserOut(BaseModel):
    """O que a API DEVOLVE sobre um usuário (nunca a senha)."""
    model_config = ConfigDict(from_attributes=True)   # aceita o objeto User do banco direto

    user_id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False
    created_at: Optional[datetime] = None