from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=False)
    
    purchases = relationship("Purchase", back_populates="user")
    products = relationship("Product", back_populates="user")
