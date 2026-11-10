from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
import jwt   # PyJWT

from core.config import settings


# ---------- Senhas ----------

def get_password(password: str) -> str:
    """Transforma a senha em hash (com salt) para guardar no banco."""
    hash_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Confere se a senha digitada corresponde ao hash guardado."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# ---------- Tokens JWT ----------

def create_access_token(subject: Any, expires_delta: Optional[timedelta] = None) -> str:
    """Cria o token de acesso (o 'crachá') do usuário."""
    if expires_delta is not None:
        expira_em = datetime.now(timezone.utc) + expires_delta
    else:
        expira_em = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    info_jwt = {"exp": expira_em, "sub": str(subject)}
    return jwt.encode(info_jwt, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)