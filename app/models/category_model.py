from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.db import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)

    products = relationship("Product", back_populates="category")