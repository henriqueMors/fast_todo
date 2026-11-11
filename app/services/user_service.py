from sqlalchemy.orm import Session
from typing import Optional
from core.security import get_password, verify_password
from models.user_models import User
from schemas.user_schema import UserAuth


class UserService:
    @staticmethod
    def create_user(session: Session, user: UserAuth) -> User:
        usuario = User(
            username=user.username,
            email=user.email,
            hash_password=get_password(user.password),
        )
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

    @staticmethod
    def authenticate(session: Session, email: str, password: str) -> Optional[User]:
        usuario = User.by_email(session, email)
        if not usuario:
            return None
        if not verify_password(password, usuario.hash_password):
            return None
        return usuario

    @staticmethod
    def get_user_by_id(session: Session, user_id) -> Optional[User]:
        return session.get(User, user_id)