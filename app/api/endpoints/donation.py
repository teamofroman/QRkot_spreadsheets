from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Список всех пожертвований',
    description='Получение списка всех пожертвований. Только администратор.',
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_include={'id', 'full_amount', 'comment', 'create_date'},
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    summary='Список пожертвований текущего пользователя',
    description='Получение списка пожертвований текущего пользователя',
)
async def get_current_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_multi(session, user)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_include={'id', 'full_amount', 'comment', 'create_date'},
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    summary='Создание пожертвования',
    description='Создание пожертвования для фонда',
)
async def create_donation(
    obj_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.create(
        obj_in,
        session,
        user,
    )
