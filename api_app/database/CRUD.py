from api_app.database.models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select
from api_app.database.databese import DatabaseHelper

"""
async def insert_user(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    User(email="efdcdswfef@f.com", password="qwerty"),
                    User(email="efefweef@f.com", password="54321")
                ]
            )


async def select_and_update_user(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        stmt = select(User).order_by(User.id)
        await session.execute(stmt)
        await session.commit()
        result = await session.execute(stmt)
        for a in result.scalars():
            print(a.email, a.password)
        # access attribute subsequent to commit; this is what
        # expire_on_commit=False allows
        # alternatively, AsyncAttrs may be used to access any attribute
        # as an awaitable (new in 2.0.13)


async def user_create() -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    # async_sessionmaker: a factory for new AsyncSession objects.
    # expire_on_commit - don't expire objects after transaction commit
    async_session = db.session_factory
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await insert_user(async_session)
    await select_and_update_user(async_session)
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()
"""