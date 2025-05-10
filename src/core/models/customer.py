"""
Customer model for storing customer information.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base


class Customer(Base):
    """Customer model for storing client information."""
    
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    company = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    notes = Column(String)
    
    # Relationship to quotes
    quotes = relationship("Quote", back_populates="customer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', company='{self.company}')>" 