from fastapi import FastAPI

from core.config import settings
from core.database import Base, engine
import models
import models.user_models import User

Base.metadata.create_all(engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)