from fastapi import APIRouter

todo_router = APIRouter()

@todo_router.get('/test')
def teste():
    return "Notas"