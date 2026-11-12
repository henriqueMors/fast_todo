from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.database import get_session
from schemas.user_schema import UserAuth, UserOut
from services.user_service import UserService

from api.dependencies.user_deps import get_current_user
from models.user_models import User

user_router = APIRouter()


@user_router.post("/adiciona", summary="Adicionar usuário",
                  response_model=UserOut, status_code=status.HTTP_201_CREATED)
def adiciona_usuario(data: UserAuth, session: Session = Depends(get_session)):
    try:
        return UserService.create_user(session, data)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ou e-mail deste usuário já existe",
        )

@user_router.get("/me", summary="Detalhes do usuário logado", response_model=UserOut)
def get_me(usuario: User = Depends(get_current_user)):
    return usuario