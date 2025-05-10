"""
Quote models for storing customer quotes and line items.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class Quote(Base):
    """Quote model for storing quote header information."""
    
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_number = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    expiration_date = Column(DateTime)
    status = Column(String, default="draft")  # "draft", "sent", "accepted", "rejected"
    notes = Column(Text)
    
    # Relationships
    customer = relationship("Customer", back_populates="quotes")
    items = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Quote(id={self.id}, quote_number='{self.quote_number}', status='{self.status}')>"
    
    @property
    def total(self):
        """Calculate total quote amount."""
        return sum(item.total for item in self.items)


class QuoteItem(Base):
    """Quote item model for storing line items in a quote."""
    
    __tablename__ = "quote_items"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)
    
    # Product configuration
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)  # Base price at time of quote
    length = Column(Float)  # Length in inches if applicable
    material = Column(String)  # Material code if applicable
    voltage = Column(String)  # Voltage specification if applicable
    description = Column(Text)  # Custom description
    
    # Pricing
    discount_percent = Column(Float, default=0.0)
    
    # Relationships
    quote = relationship("Quote", back_populates="items")
    product = relationship("ProductVariant", back_populates="quote_items")
    options = relationship("QuoteItemOption", back_populates="quote_item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<QuoteItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
    
    @property
    def options_total(self):
        """Calculate total for all options."""
        return sum(option.price * option.quantity for option in self.options)
    
    @property
    def subtotal(self):
        """Calculate subtotal before discount."""
        return (self.unit_price * self.quantity) + self.options_total
    
    @property
    def discount_amount(self):
        """Calculate discount amount."""
        return self.subtotal * (self.discount_percent / 100)
    
    @property
    def total(self):
        """Calculate total for this line item with discount applied."""
        return self.subtotal - self.discount_amount 