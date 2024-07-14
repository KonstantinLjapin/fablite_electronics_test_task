from api_app.database.models import Base, User
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select, update
from api_app.database.databese import DatabaseHelper
from api_app.database import schemas


async def insert_user(async_session: async_sessionmaker[AsyncSession], user: schemas.UserCreate) -> None:
    """Добавление пользователя в сессию ОРМ"""
    async with async_session() as session:
        async with session.begin():
            session.add(User(email=user.email, password=user.password))


async def select_and_update_user(async_session: async_sessionmaker[AsyncSession]) -> None:
    """Обновление пользователя в сессии ОРМ"""
    async with async_session() as session:
        stmt = select(User).order_by(User.id)
        await session.execute(stmt)
        await session.commit()


async def get_all_users() -> list:
    """получение списка пользователей"""
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
    """Создание пользователя """
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async_session = db.session_factory
    await insert_user(async_session, user)
    await select_and_update_user(async_session)
    await engine.dispose()


async def user_update(old_user: schemas.UserCreate, new_user: schemas.UserCreate) -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async_session = db.session_factory
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).order_by(User.id))
            temp_id: int
            for r in result.scalars().all():
                if r.email == old_user.email:
                    temp_id = int(r.id)
            stmt = (
                update(User)
                .where(User.id == temp_id)
                .values(email=new_user.email, password=new_user.password)
            )
            await session.execute(stmt)
            await session.commit()
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
