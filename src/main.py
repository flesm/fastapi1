from fastapi import FastAPI

from auth.schemas import UserRead, UserCreate

from operations.router import router as router_operation
from auth.base_config import fastapi_users, auth_backend

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


# create asynccontextmanager that will customize and clean resources of cache
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Trading App",
    lifespan=lifespan,  # for cache
)


@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="world!")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
