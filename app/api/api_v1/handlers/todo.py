from typing import List

from fastapi import APIRouter, Depends

from api.dependencies.user_deps import get_current_user
from models.user_models import User
from schemas.todo_schema import TodoDetail

todo_router = APIRouter()


@todo_router.get('/', summary="Lista Todas as Notas", response_model=List[TodoDetail])
def listar(current_user: User = Depends(get_current_user)):
    pass