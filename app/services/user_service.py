from sqlalchemy.orm import Session
from core.security import get_password
from models.user_models import User
from schemas.user_schema import UserAuth


class UserService:
    @staticmethod
    def create_user(session: Session, user: UserAuth) -> User:
        usuario = User(
            username=user.username,
            email=user.email,
            hash_password=get_password(user.password),   # PROVISÓRIO: vira hash quando a aula de segurança chegar
        )
        session.add(usuario)
        session.commit()
        session.refresh(usuario)           # traz o user_id e o created_at gerados
        return usuario