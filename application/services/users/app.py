from fastapi import APIRouter, FastAPI

app = FastAPI(title="Users API")
router = APIRouter(prefix="/users", tags=["User"])


@router.get("/users")
async def get_users():
    raise NotImplementedError


@router.get("/users/search")
async def search_users(query: str):
    # Логика для поиска пользователей
    raise NotImplementedError


app.include_router(router)
