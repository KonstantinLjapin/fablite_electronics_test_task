import uvicorn
import asyncio
from database.CRUD import user_create, base_create, get_all_users, user_delete
from fastapi import FastAPI, HTTPException
from api_app.database import schemas
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/list_user", response_model=list[schemas.UserCreate])
async def get_list_users():
    out = await get_all_users()
    return out


@app.post("/create_user")
async def create_user(user: schemas.UserCreate):
    # schemas.UserCreate(email="efdcdswfef@f.com", password="qwerty")
    await user_create(user)
    return {"Hello": "World"}


@app.put("/update_user")
async def update_user():
    return {"Hello": "World"}


@app.delete("/delete_user")
async def delete_user(user: schemas.User):
    result: bool = await user_delete(user)
    if result:
        return {"ok": True}
    else:
        raise HTTPException(status_code=404, detail="user not found")


if __name__ == "__main__":
    # создаются таблицы в бд
    asyncio.run(base_create())
    # запуск сервера
    uvicorn.run(app, host="0.0.0.0", port=8000)
