"""
Configuración de sesión de base de datos.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings

# Motor asíncrono
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
)

# Sesión asíncrona
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    """Dependency para obtener sesión de base de datos."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
