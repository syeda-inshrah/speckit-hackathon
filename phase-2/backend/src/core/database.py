from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.core.config import settings


def get_async_database_url(url: str) -> str:
    """
    Convert PostgreSQL URL to async format for asyncpg driver.
    Handles both ssl=require and sslmode=require formats.
    """
    # If already has asyncpg, return as is
    if "postgresql+asyncpg://" in url:
        return url

    # Replace postgresql:// with postgresql+asyncpg://
    async_url = url.replace("postgresql://", "postgresql+asyncpg://")

    # Convert sslmode=require to ssl=require for asyncpg
    async_url = async_url.replace("sslmode=require", "ssl=require")

    # Remove channel_binding if present (not supported by asyncpg)
    if "channel_binding=" in async_url:
        parts = async_url.split("&")
        async_url = "&".join([p for p in parts if not p.startswith("channel_binding=")])

    return async_url


# Create async engine with proper URL format
try:
    database_url = get_async_database_url(settings.DATABASE_URL)
    engine: AsyncEngine = create_async_engine(
        database_url,
        echo=False,  # Set to False to reduce log noise
        future=True,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,
        max_overflow=10,
    )
except Exception as e:
    print(f"ERROR: Failed to create database engine: {e}")
    print(f"       DATABASE_URL format: {settings.DATABASE_URL[:50]}...")
    raise

# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """Dependency for getting async database session"""
    async with async_session_maker() as session:
        yield session


async def init_db() -> None:
    """Initialize database tables (for development only)"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
