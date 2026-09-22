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
        back_populates="store"
    )
