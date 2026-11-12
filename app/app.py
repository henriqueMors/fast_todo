from fastapi import FastAPI
from core.config import settings
from core.database import Base, engine
from models.user_models import User
from api.api_v1.router import router
from models.todo_models import Todo

Base.metadata.create_all(engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(
    router,
    prefix=settings.API_V1_STR
)