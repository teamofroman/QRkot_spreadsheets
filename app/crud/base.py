from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.services.investing import process_invest


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_multi(
        self,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        query = select(self.model)

        if user:
            query = query.where(self.model.user_id == user.id)

        db_objs = await session.execute(query)
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()

        if user:
            obj_in_data['user_id'] = user.id

        db_obj = self.model(**obj_in_data)

        session.add(db_obj)
        await session.commit()

        await session.refresh(db_obj)
        await process_invest(db_obj, session)

        await session.refresh(db_obj)

        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ):
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()
