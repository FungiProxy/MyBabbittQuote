"""
Product family and variant models for storing product information.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class ProductFamily(Base):
    """Product family model for grouping related products."""
    
    __tablename__ = "product_families"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)  # e.g., "LS2000", "LS7000"
    description = Column(Text)
    category = Column(String, index=True)  # e.g., "Level Switch", "Transmitter"
    
    # Relationships
    variants = relationship("ProductVariant", back_populates="product_family")
    spare_parts = relationship("SparePart", back_populates="product_family")
    
    def __repr__(self):
        return f"<ProductFamily(id={self.id}, name='{self.name}', category='{self.category}')>"


class ProductVariant(Base):
    """Product variant model for storing specific product configurations."""
    
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_family_id = Column(Integer, ForeignKey("product_families.id"), nullable=False)
    model_number = Column(String, nullable=False, index=True)  # e.g., "LS2000-115VAC-S-10\""
    description = Column(Text)
    
    # Pricing information
    base_price = Column(Float, nullable=False, default=0.0)
    base_length = Column(Float)  # Base length in inches
    
    # Configuration options
    voltage = Column(String)  # e.g., "115VAC", "24VDC"
    material = Column(String)  # e.g., "S", "H", "U", "T"
    
    # Relationships
    product_family = relationship("ProductFamily", back_populates="variants")
    quote_items = relationship("QuoteItem", back_populates="product")
    
    def __repr__(self):
        return f"<ProductVariant(id={self.id}, model='{self.model_number}', base_price={self.base_price})>" 