from sqlalchemy import Column, String, Integer, Boolean, Text, func, DateTime, ForeignKey
from app.core.database import Base
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModels(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)

    stores = relationship("StoresModel", back_populates="owner")  
      
    managed_stores = relationship(
    "StoreManagerModels",
    back_populates="owner"
    )

    def hash_password(self, plain_password: str) -> str:
        """Hashes the given password using bcrypt."""
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        """Verifies the given password against the stored hash."""
        return pwd_context.verify(plain_password, self.password)
    
    def set_password(self, plain_text: str) ->  None :
        self.password = self.hash_password(plain_text)