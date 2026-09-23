from sqlalchemy import Column, String, Integer, Boolean, Text, func, DateTime, ForeignKey, CheckConstraint
from app.core.database import Base
from sqlalchemy.orm import relationship


class SalesModels(Base):
    __tablename__ = "sales"

    id = Column(Integer, autoincrement=True, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)
    amount = Column(Integer, CheckConstraint("amount > 0"), nullable=True)
    sales_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    create_at = Column(DateTime, server_default=func.now(), nullable=False)