from sqlalchemy import Column, String

from app.core.constants import MAX_NAME_LENGTH
from app.core.db import Base
from app.models.financial_base import FinancialBase


class CharityProject(Base, FinancialBase):
    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(String, nullable=False)
