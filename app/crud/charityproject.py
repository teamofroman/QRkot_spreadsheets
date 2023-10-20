from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, User

from .validators import (check_charity_project_before_edit,
                         check_charity_project_invested,
                         check_charity_project_is_closed,
                         check_charity_project_name_duplicate)


class CRUDCharityProject(CRUDBase):
    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        await check_charity_project_name_duplicate(obj_in.name, session, self)

        return await super().create(obj_in, session, user)

    async def update(self, db_obj, obj_in, session: AsyncSession):
        await check_charity_project_before_edit(
            **obj_in.dict(),
            charity_project=db_obj,
            session=session,
            crud=self,
        )

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if update_data.get('full_amount', None):
            if update_data['full_amount'] == db_obj.invested_amount:
                setattr(db_obj, 'close_date', datetime.now())
                setattr(db_obj, 'fully_invested', True)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession):
        await check_charity_project_invested(db_obj)

        await check_charity_project_is_closed(db_obj)

        await session.delete(db_obj)
        await session.commit()

        return db_obj


charity_project_crud = CRUDCharityProject(CharityProject)
