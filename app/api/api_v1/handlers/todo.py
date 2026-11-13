from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.dependencies.user_deps import get_current_user
from core.database import get_session
from models.user_models import User
from schemas.todo_schema import TodoCreate, TodoDetail
from services.todo_service import TodoService

todo_router = APIRouter()


@todo_router.get('/', summary="Listar Todas as Notas", response_model=List[TodoDetail])
def listar(current_user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    return TodoService.list_todos(session, current_user)


@todo_router.post('/create', summary="Adicionando Nota", response_model=TodoDetail,
                  status_code=status.HTTP_201_CREATED)
def create_todo(data: TodoCreate, current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    return TodoService.create_todo(session, current_user, data)