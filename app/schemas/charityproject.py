from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Extra, Field, NonNegativeInt, PositiveInt,
                      root_validator)

from app.core.constants import DEFAULT_AMOUNT, MAX_NAME_LENGTH, MIN_LENGTH


class CharityProjectBase(BaseModel):
    """Базовый класс для схем проекта"""

    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH,
        max_length=MAX_NAME_LENGTH,
    )
    description: Optional[str] = Field(None, min_length=MIN_LENGTH)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    """Схема для вывода информации о проекте из БД"""

    id: int
    invested_amount: NonNegativeInt = Field(DEFAULT_AMOUNT)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config(CharityProjectBase.Config):
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта"""

    name: str = Field(None, min_length=MIN_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(None, min_length=MIN_LENGTH)
    full_amount: PositiveInt

    @root_validator(skip_on_failure=True)
    def params_can_not_be_null(cls, values):  # noqa
        if values.get('name', None) is None:
            raise ValueError('Имя проекта не может быть пустым!')

        if values.get('description', None) is None:
            raise ValueError('Описание проекта не может быть пустым!')

        return values


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления проекта"""

    ...
