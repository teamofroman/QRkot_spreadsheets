from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists_by_id(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get_by_attribute(
        'id', charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(status_code=422, detail='Проект не найден.')

    return charity_project
