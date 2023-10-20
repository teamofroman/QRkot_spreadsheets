import contextlib
from datetime import datetime
from random import randint, random

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.models import CharityProject, Donation
from app.schemas.user import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: EmailStr, password: str, is_superuser: bool = False
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    if (
        settings.first_superuser_email is not None and
            settings.first_superuser_password is not None
    ):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )


async def create_sample_charity_projects():
    async with get_async_session_context() as session:
        for i in range(10):
            charity_project = CharityProject(
                name=f'Project {i} {datetime.now()}',
                description=f'Sample project {i}',
                full_amount=randint(1, 100),
            )

            if random() > 0.6:
                setattr(
                    charity_project,
                    'invested_amount',
                    charity_project.full_amount,
                )
                setattr(charity_project, 'fully_invested', True)
                setattr(charity_project, 'close_date', datetime.now())

            session.add(charity_project)
            await session.commit()

    print('Sample charity project was created...')


async def create_sample_donation():
    async with get_async_session_context() as session:
        for i in range(10):
            donation = Donation(
                comment=f'Donation {i} {datetime.now()}',
                full_amount=randint(1, 100),
            )

            if random() > 0.6:
                setattr(
                    donation,
                    'invested_amount',
                    donation.full_amount,
                )
                setattr(donation, 'fully_invested', True)
                setattr(donation, 'close_date', datetime.now())

            session.add(donation)
            await session.commit()

    print('Sample donation was created...')


async def create_sample_data():
    if settings.create_sample_data:
        await create_sample_charity_projects()
        await create_sample_donation()
