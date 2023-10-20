from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.constants import DEFAULT_AMOUNT


class FinancialBase:
    __abstract__ = True
    full_amount = Column(Integer, default=DEFAULT_AMOUNT, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime, default=None)
