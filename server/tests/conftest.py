from functools import lru_cache
from pathlib import Path
from httpx import ASGITransport, AsyncClient
from pydantic_settings import BaseSettings, SettingsConfigDict
import pytest_asyncio
from server.database import get_session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel
from server.main import app
from server.settings.config import get_settings


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env.test", extra="allow"
    )


@lru_cache()
def get_test_settings() -> TestSettings:
    return TestSettings()


settings = get_test_settings()
database_url = settings.database_url
engine = create_async_engine(database_url, echo=False)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def get_test_session():
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_settings] = get_test_settings
app.dependency_overrides[get_session] = get_test_session


@pytest_asyncio.fixture(scope="function")
async def setup_database():
    await create_db_and_tables()
    yield
    await drop_db_and_tables()
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
