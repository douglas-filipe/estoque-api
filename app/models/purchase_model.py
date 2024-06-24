from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database.db import Base

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    purchase_date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False) 

    product = relationship("Product", back_populates="purchases")
    user = relationship("User", back_populates="purchases")