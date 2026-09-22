from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship
class StoreManagerModels(Base):
    __tablename__ = "store_manager"

    id = Column(Integer, autoincrement=True, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    is_active = Column(Boolean, default=True)

    create_at = Column(DateTime, server_default=func.now(), nullable=False)
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now() , nullable=False)

    owner_store_manager = relationship("UserModels", back_populates="managed_stores")
    store_id_store_manager = relationship("StoresModel", back_populates="managers")