from contextlib import asynccontextmanager
from backend.database import create_tables

@asynccontextmanager
async def lifespan(app):
    create_tables()
    yield