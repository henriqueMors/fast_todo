from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.database import get_session
from schemas.user_schema import UserAuth, UserOut
from services.user_service import UserService

user_router = APIRouter()


@user_router.post("/adiciona", summary="Adiciona usuário",
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