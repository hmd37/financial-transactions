from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import init_db
from .routers import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/api", tags=["Users"])
