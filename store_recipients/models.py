from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base



class StoreRecipientModel(Base):
    __tablename__ = "store_recipients"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    create_at = Column(DateTime, server_default=func.now(), nullable=False)
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now() , nullable=False)

    # Relationships
    stores_back_populates_to_recipient = relationship("StoresModel", back_populates="recipient")