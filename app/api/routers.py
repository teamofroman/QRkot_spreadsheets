from fastapi import APIRouter

from app.api.endpoints import (charity_project_router, donation_router,
                               user_router)

api_router = APIRouter()

api_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['charity projects'],
)

api_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['donation'],
)

api_router.include_router(user_router)
