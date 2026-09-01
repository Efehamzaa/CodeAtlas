from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Proje dizininde codeatlas.db adında bir dosya oluşturur
DATABASE_URL = "sqlite+aiosqlite:///./codeatlas.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session