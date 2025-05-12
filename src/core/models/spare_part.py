"""
Spare parts model for storing spare part information.
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Base


class SparePart(Base):
    """Spare part model for storing spare parts and their pricing."""
    
    __tablename__ = "spare_parts"
    
    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Pricing information
    price = Column(Float, nullable=False, default=0.0)
    
    # Related product family
    product_family_id = Column(Integer, ForeignKey("product_families.id"))
    
    # Categorization
    category = Column(String, index=True)  # e.g., "electronics", "probe_assembly", "housing"
    
    # Relationships
    product_family = relationship("ProductFamily", back_populates="spare_parts")
    
    def __repr__(self):
        return f"<SparePart(id={self.id}, part_number='{self.part_number}', name='{self.name}', price={self.price})>" 