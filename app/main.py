from fastapi import FastAPI

from app.api.routers import api_router
from app.core.config import settings
from app.core.init_db import create_first_superuser, create_sample_data

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(api_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
    await create_sample_data()
