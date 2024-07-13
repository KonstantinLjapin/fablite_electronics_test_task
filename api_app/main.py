import uvicorn
import asyncio
from database.CRUD import user_create, base_create, get_all_users
from fastapi import FastAPI
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/list_user")
async def get_list_users():
    out = await get_all_users()
    return {"Users": out}


@app.post("/create_user")
async def create_user():
    await user_create()
    return {"Hello": "World"}


@app.put("/update_user")
async def update_user():
    return {"Hello": "World"}

if __name__ == "__main__":
    # создаются таблицы в бд
    asyncio.run(base_create())
    # запуск сервера
    uvicorn.run(app, host="0.0.0.0", port=8000)
