from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt

from app.core.constants import MIN_LENGTH


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = Field(None, min_length=MIN_LENGTH)

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    ...


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]

    class Config(DonationBase.Config):
        orm_mode = True
