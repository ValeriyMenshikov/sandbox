from fastapi import FastAPI, APIRouter

app = FastAPI(title="Users API")
router = APIRouter(prefix="/users", tags=["User"])


@router.get("/item")
async def read_item2():
    return {"item": "This is from Service 2"}
app.include_router(router)
