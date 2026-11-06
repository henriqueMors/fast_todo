from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_session():
    """Abre uma sessão por requisição e fecha no final."""
    with SessionLocal() as session:
        yield session