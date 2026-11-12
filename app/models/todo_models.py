import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from core.database import Base


def agora():
    return datetime.now(timezone.utc)


class Todo(Base):
    __tablename__ = "todos"

    todo_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    status = Column(Boolean, default=False)
    title = Column(String(100), nullable=False, index=True)
    description = Column(String(1000), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=agora)
    updated_at = Column(DateTime(timezone=True), default=agora, onupdate=agora)

    owner_id = Column(Uuid, ForeignKey("users.user_id"), nullable=False, index=True)
    owner = relationship("User", back_populates="todos")

    def __repr__(self) -> str:
        return f"<Todo {self.title}>"

    def __str__(self) -> str:
        return self.title