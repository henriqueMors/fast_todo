from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from models.todo_models import Todo
from models.user_models import User
from schemas.todo_schema import TodoCreate


class TodoService:
    @staticmethod
    def list_todos(session: Session, user: User) -> List[Todo]:
        return session.query(Todo).filter(Todo.owner_id == user.user_id).all()

    @staticmethod
    def create_todo(session: Session, user: User, data: TodoCreate) -> Todo:
        todo = Todo(**data.model_dump(), owner_id=user.user_id)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    
    @staticmethod
    def detail(session: Session, user: User, todo_id: UUID) -> Optional[Todo]:
        return (session.query(Todo)
                .filter(Todo.todo_id == todo_id, Todo.owner_id == user.user_id)
                .first())

    @staticmethod
    def update_todo(session: Session, user: User, todo_id: UUID, data: TodoUpdate) -> Optional[Todo]:
        todo = TodoService.detail(session, user, todo_id)
        if not todo:
            return None
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(todo, campo, valor)
        session.commit()
        session.refresh(todo)
        return todo