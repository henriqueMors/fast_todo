from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TodoCreate(BaseModel):
    """O que a API RECEBE para criar uma nota."""
    title: str = Field(..., min_length=1, max_length=100, description="Título da nota")
    description: str = Field(..., min_length=1, max_length=1000, description="Descrição da nota")
    status: Optional[bool] = False


class TodoUpdate(BaseModel):
    """O que a API RECEBE para atualizar: tudo opcional."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[bool] = None


class TodoDetail(BaseModel):
    """O que a API DEVOLVE sobre uma nota."""
    model_config = ConfigDict(from_attributes=True)

    todo_id: UUID
    status: bool
    title: str
    description: str
    created_at: datetime
    updated_at: datetime