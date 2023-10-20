from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.db import Base
from app.models.financial_base import FinancialBase


class Donation(Base, FinancialBase):
    comment = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
