from typing import Any
from core.security import create_access_token, create_refresh_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_session
from services.user_service import UserService

auth_router = APIRouter()


@auth_router.post('/login', summary="Login do usuário")
def login(data: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)) -> Any:
    usuario = UserService.authenticate(
        session,
        email=data.username,          # o formulário OAuth2 chama o campo de "username"
        password=data.password,
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou senha incorretos",
        )
        return {
        "access_token": create_access_token(usuario.user_id),
        "refresh_token": create_refresh_token(usuario.user_id),
    }