
import os
import urllib.parse
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from src.infrastructure.db import Base  
from src.infrastructure import models   

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/app_test",
)

def _split_base_and_db(async_url: str) -> tuple[str, str]:
    """
    Troca +asyncpg por síncrono só para parsear, separa o nome do DB
    e retorna a URL apontando para o catálogo 'postgres'.
    """
    u = urllib.parse.urlparse(async_url.replace("+asyncpg", ""))
    dbname = u.path.lstrip("/")
    base_sync = u._replace(path="/postgres").geturl()
    
    base_async = base_sync.replace("postgresql://", "postgresql+asyncpg://")
    return base_async, dbname

@pytest_asyncio.fixture(scope="session")
async def engine():
    
    if TEST_DATABASE_URL.startswith("postgresql+asyncpg://"):
        base_async, dbname = _split_base_and_db(TEST_DATABASE_URL)
        admin_engine = create_async_engine(
            base_async,
            isolation_level="AUTOCOMMIT",  
            future=True,
            poolclass=NullPool,
        )
        try:
            async with admin_engine.begin() as conn:
                await conn.exec_driver_sql(f'CREATE DATABASE "{dbname}"')
        except Exception:
            
            pass
        finally:
            await admin_engine.dispose()

   
    eng = create_async_engine(TEST_DATABASE_URL, future=True, poolclass=NullPool)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()

@pytest_asyncio.fixture()
async def session(engine) -> AsyncSession:
    factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    async with factory() as s:
        async with s.begin():
            yield s 

# ---------- factories ----------
from src.infrastructure.models import ProductORM, CustomerORM

@pytest_asyncio.fixture()
async def mk_product(session: AsyncSession):
    async def _f(**over):
        kwargs = {
            "name": "P",
            "sku": f"SKU-{os.urandom(2).hex()}",
            "price": 1990,
            "stock_qty": 50,
            "is_active": True,
        }
        kwargs.update(over)
        p = ProductORM(**kwargs)
        session.add(p)
        await session.flush()
        return p
    return _f

@pytest_asyncio.fixture()
async def mk_customer(session: AsyncSession):
    async def _f(**over):
        kwargs = {
            "name": "Cliente",
            "email": f"c{os.urandom(2).hex()}@mail.com",
            "document": f"000{os.urandom(2).hex()}",
        }
        kwargs.update(over)
        c = CustomerORM(**kwargs)
        session.add(c)
        await session.flush()
        return c
    return _f
