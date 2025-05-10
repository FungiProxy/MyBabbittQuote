"""
Material model for storing product material information and pricing rules.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class Material(Base):
    """Material model for storing material codes and pricing rules."""
    
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, index=True, unique=True)  # e.g., "S", "H", "U", "T"
    name = Column(String, nullable=False)  # Full name, e.g., "316 Stainless Steel"
    description = Column(Text)
    
    # Pricing information
    base_length = Column(Float, nullable=False)  # Standard base length in inches
    length_adder_per_inch = Column(Float)  # Additional cost per inch
    length_adder_per_foot = Column(Float)  # Additional cost per foot
    
    # Special pricing rules
    has_nonstandard_length_surcharge = Column(Boolean, default=False)
    nonstandard_length_surcharge = Column(Float, default=0.0)
    base_price_adder = Column(Float, default=0.0)  # Amount to add to base price
    
    def __repr__(self):
        return f"<Material(code='{self.code}', name='{self.name}')>"
    
    
class StandardLength(Base):
    """Standard lengths for materials that have non-standard length surcharges."""
    
    __tablename__ = "standard_lengths"
    
    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String, nullable=False, index=True)
    length = Column(Float, nullable=False)  # Length in inches
    
    def __repr__(self):
        return f"<StandardLength(material='{self.material_code}', length={self.length})>" 