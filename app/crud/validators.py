from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


async def check_charity_project_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
    crud: CRUDBase,
) -> None:
    charity_project = await crud.get_by_attribute(
        'name', charity_project_name, session
    )

    if charity_project:
        raise HTTPException(
            status_code=400, detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_is_closed(
    charity_project: CharityProject,
):
    if charity_project.close_date:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_charity_project_invested(
    charity_project: CharityProject,
):
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_charity_project_before_edit(**kwargs):
    if kwargs['charity_project'].close_date:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )
    if kwargs.get('name', None):
        await check_charity_project_name_duplicate(
            kwargs['name'],
            kwargs['session'],
            kwargs['crud'],
        )

    if kwargs.get('full_amount', None):
        if kwargs['full_amount'] < kwargs['charity_project'].invested_amount:
            raise HTTPException(
                status_code=422,
                detail=(
                    'Нельзя сумму проекта сделать меньше, чем уже '
                    'инвестировано'
                ),
            )
