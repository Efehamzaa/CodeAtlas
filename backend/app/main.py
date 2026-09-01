from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import health, repository, scanner
from app.core.database import engine
from app.models.base import Base


import app.models.core
import app.models.analysis
import app.models.findings
import app.models.knowledge

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Sunucu ayağa kalkarken tabloları PostgreSQL'de yarat
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Sunucu kapanırken motoru temizle
    await engine.dispose()

app = FastAPI(
    title="CodeAtlas",
    description="Understand Any Repository",
    version="0.1.0",
    lifespan=lifespan  # Yaşam döngüsünü uygulamaya bağladık
)

app.include_router(health.router)
app.include_router(repository.router)
app.include_router(scanner.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CodeAtlas"
    }


         