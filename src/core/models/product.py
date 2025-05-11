"""
Product model for storing product information.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class Product(Base):
    """Product model for storing specific product configurations."""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    model_number = Column(String, nullable=False, index=True)  # e.g., "LS2000", "LS8000/2"
    description = Column(Text)
    category = Column(String, index=True)  # e.g., "Level Switch", "Transmitter"
    
    # Pricing information
    base_price = Column(Float, nullable=False, default=0.0)
    base_length = Column(Float)  # Base length in inches
    
    # Configuration options
    voltage = Column(String)  # e.g., "115VAC", "24VDC"
    material = Column(String)  # e.g., "S", "H", "U", "T"
    
    # No relationships with QuoteItem - it now relates to ProductVariant
    
    def __repr__(self):
        return f"<Product(id={self.id}, model='{self.model_number}', base_price={self.base_price})>"            