from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_maker = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
