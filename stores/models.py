from sqlalchemy import Column, String, Integer, Boolean, Text, func, DateTime, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class StoresModel(Base):
    __tablename__ = "stores"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(150), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("UserModels", back_populates="stores")

    managers = relationship(
        "StoreManagerModels",
        back_populates="store_id_store_manager"
    )

    stores_back_populates = relationship("SalesModels", back_populates="sales")

    stores_back_populates_to_expenses = relationship("ExpensesModels", back_populates="expenses")