from api_app.database.models import Base, User
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from api_app.database.databese import DatabaseHelper


async def insert_user(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    User(email="efdcdswfef@f.com", hashed_password="qwerty"),
                    User(email="efefweef@f.com", hashed_password="54321")
                ]
            )


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
            out.append(a.email)
    await engine.dispose()
    return out


async def user_create() -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async_session = db.session_factory
    await insert_user(async_session)
    await select_and_update_user(async_session)
    await engine.dispose()


async def base_create() -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("database created")