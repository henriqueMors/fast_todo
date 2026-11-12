import uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, String, Uuid

from core.database import Base


class User(Base):
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")
    __tablename__ = "users"

    user_id = Column(Uuid, primary_key=True, default=uuid.uuid4)          # UUID gerado sozinho
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hash_password = Column(String(255), nullable=False)                    # nunca a senha em texto
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))         # data de criação

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    @classmethod
    def by_email(cls, session, email: str) -> "User":
        return session.query(cls).filter(cls.email == email).first()