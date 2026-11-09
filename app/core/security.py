import bcrypt


def get_password(password: str) -> str:
    """Transforma a senha em hash (com salt) para guardar no banco."""
    hash_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Confere se a senha digitada corresponde ao hash guardado."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))