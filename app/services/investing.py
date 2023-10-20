from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import not_

from app.models import CharityProject, Donation


async def get_db_objects(
    objects_type,
    session: AsyncSession,
):
    db_objects = await session.execute(
        select(objects_type)
        .where(not_(objects_type.fully_invested))
        .order_by('create_date')
    )

    return db_objects.scalars().all()


def invest(project: CharityProject, donation: Donation):
    available_invest = donation.full_amount - donation.invested_amount
    need_invest = project.full_amount - project.invested_amount

    project.invested_amount += min(need_invest, available_invest)
    donation.invested_amount += min(need_invest, available_invest)

    project.fully_invested = project.invested_amount == project.full_amount
    donation.fully_invested = donation.invested_amount == donation.full_amount


async def process_invest(create_object, session: AsyncSession):
    if not isinstance(create_object, (CharityProject, Donation)):
        return

    process_type = (
        Donation
        if isinstance(create_object, CharityProject)
        else CharityProject
    )

    available_objects = await get_db_objects(process_type, session)

    if not available_objects:
        return

    while available_objects and not create_object.fully_invested:
        current_object = available_objects.pop(0)

        if process_type is Donation:
            invest(create_object, current_object)
        else:
            invest(current_object, create_object)

        if current_object.fully_invested:
            current_object.close_date = datetime.now()

        if create_object.fully_invested:
            create_object.close_date = datetime.now()

        session.add(current_object)
        session.add(create_object)

    await session.commit()
