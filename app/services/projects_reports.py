from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject


async def get_closed_project(session: AsyncSession):
    closed_projects = await session.execute(
        select(
            CharityProject.name,
            (func.julianday(CharityProject.close_date) -
             func.julianday(CharityProject.create_date)).label('rate'),
            CharityProject.description,
        ).where(CharityProject.fully_invested)
        .order_by('rate')
    )

    return closed_projects.all()


async def get_projects_by_completion_rate(session: AsyncSession):
    closed_projects = await get_closed_project(session)

    return [
        {
            'name': close_project.name,
            'completion_rate': timedelta(close_project.rate),
            'description': close_project.description,
        }
        for close_project in closed_projects
    ]
