import jwt   # PyJWT
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_session
from models.user_models import User
from schemas.auth_schema import TokenPayload
from services.user_service import UserService

oauth_reusavel = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT",
)


def get_current_user(
    token: str = Depends(oauth_reusavel),
    session: Session = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Erro na validação do token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = UserService.get_user_by_id(session, token_data.sub)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível encontrar o usuário",
        )
    return usuario