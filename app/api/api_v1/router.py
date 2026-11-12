from fastapi import APIRouter
from api.api_v1.handlers import user
from api.auth import jwt
from api.api_v1.handlers import todo

router = APIRouter()

router.include_router(user.user_router, prefix='/users', tags=['users'])
router.include_router(jwt.auth_router, prefix='/auth', tags=['auth'])
router.include_router(todo.todo_router, prefix='/todo', tags=['todo'])