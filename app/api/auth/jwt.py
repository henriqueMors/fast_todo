import jwt   # PyJWT
from typing import Any
from core.security import create_access_token, create_refresh_token
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from pydantic import ValidationError
from core.database import get_session
from services.user_service import UserService



from core.config import settings
from schemas.auth_schema import TokenPayload, TokenSchema

auth_router = APIRouter()


@auth_router.post('/login', summary="Login do usuário", response_model=TokenSchema)
def login(data: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)) -> Any:
    usuario = UserService.authenticate(
        session,
        email=data.username,
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
        "token_type": "bearer",
    }

@auth_router.post('/refresh', summary="Refresh Token", response_model=TokenSchema)
def refresh_token(refresh_token: str = Body(..., embed=True),
                  session: Session = Depends(get_session)) -> Any:
    try:
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH_SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = UserService.get_user_by_id(session, token_data.sub)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível encontrar o usuário",
        )

    return {
        "access_token": create_access_token(usuario.user_id),
        "refresh_token": create_refresh_token(usuario.user_id),
        "token_type": "bearer",
    }