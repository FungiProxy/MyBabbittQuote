"""
Option model for storing product add-ons and their pricing.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Base


class Option(Base):
    """Option model for storing product add-ons and their pricing."""
    
    __tablename__ = "options"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    
    # Pricing information
    price = Column(Float, nullable=False, default=0.0)
    price_type = Column(String, default="fixed")  # "fixed", "per_inch", "per_foot"
    
    # Option category
    category = Column(String, index=True)  # e.g., "mounting", "material", "feature"
    
    # Compatibility
    product_families = Column(String)  # Comma-separated list of compatible product families
    excluded_products = Column(String)  # Comma-separated list of incompatible products
    
    def __repr__(self):
        return f"<Option(id={self.id}, name='{self.name}', price={self.price})>"


class QuoteItemOption(Base):
    """Junction table for tracking options added to quote items."""
    
    __tablename__ = "quote_item_options"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_item_id = Column(Integer, ForeignKey("quote_items.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("options.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)  # Price at time of quote
    
    # Relationships
    quote_item = relationship("QuoteItem", back_populates="options")
    option = relationship("Option")
    
    def __repr__(self):
        return f"<QuoteItemOption(id={self.id}, option_id={self.option_id}, price={self.price})>" 