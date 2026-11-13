from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.user_deps import get_current_user
from core.database import get_session
from models.user_models import User
from schemas.todo_schema import TodoCreate, TodoDetail, TodoUpdate
from services.todo_service import TodoService

todo_router = APIRouter()

NAO_ENCONTRADA = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota não encontrada")


@todo_router.get('/', summary="Lista Todas as Notas", response_model=List[TodoDetail])
def listar(current_user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    return TodoService.list_todos(session, current_user)


@todo_router.post('/create', summary="Adicionando Nota", response_model=TodoDetail,
                  status_code=status.HTTP_201_CREATED)
def create_todo(data: TodoCreate, current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    return TodoService.create_todo(session, current_user, data)


@todo_router.get('/{todo_id}', summary='Detalhe de Nota por Id', response_model=TodoDetail)
def detail(todo_id: UUID, current_user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    todo = TodoService.detail(session, current_user, todo_id)
    if not todo:
        raise NAO_ENCONTRADA
    return todo


@todo_router.put('/{todo_id}', summary='Atualiza Nota', response_model=TodoDetail)
def update(todo_id: UUID, data: TodoUpdate, current_user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    todo = TodoService.update_todo(session, current_user, todo_id, data)
    if not todo:
        raise NAO_ENCONTRADA
    return todo


@todo_router.delete('/{todo_id}', summary='Exclui Nota', status_code=status.HTTP_204_NO_CONTENT)
def delete(todo_id: UUID, current_user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    if not TodoService.delete_todo(session, current_user, todo_id):
        raise NAO_ENCONTRADA