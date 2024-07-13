from api_app.database.models import Base, User
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from api_app.database.databese import DatabaseHelper
from api_app.database import schemas


async def insert_user(async_session: async_sessionmaker[AsyncSession], user: schemas.UserCreate) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add(User(email=user.email, password=user.password))


async def select_and_update_user(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        stmt = select(User).order_by(User.id)
        await session.execute(stmt)
        await session.commit()


async def get_all_users() -> list:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async_session = db.session_factory
    out: list = []
    async with async_session() as session:
        stmt = select(User).order_by(User.id)
        result = await session.execute(stmt)
        for a in result.scalars():
            out.append(schemas.UserCreate(email=a.email, password=a.password))
    await engine.dispose()
    return out


async def user_create(user: schemas.UserCreate) -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async_session = db.session_factory
    await insert_user(async_session, user)
    await select_and_update_user(async_session)
    await engine.dispose()


async def user_update(old_user: schemas.UserCreate, nev_user: schemas.UserCreate) -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async_session = db.session_factory
    await insert_user(async_session, old_user)
    await select_and_update_user(async_session)
    await engine.dispose()


async def user_delete(shema_user: schemas.User) -> bool:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async_session = db.session_factory
    out: bool = True
    async with async_session() as session:
        user = await session.get(User, shema_user.id)
        if not user:
            out = False
        await session.delete(user)
        await session.commit()
    await engine.dispose()
    return out


async def base_create() -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
