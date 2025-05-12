from sqlalchemy import Column, Integer, String, Float
from src.core.database import Base

class ConnectionOption(Base):
    __tablename__ = "connection_options"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # "Flange" or "Tri-Clamp"
    rating = Column(String, nullable=True)  # "150#", "300#", or None for Tri-Clamp
    size = Column(String, nullable=False)   # e.g., '1"', '1.5"', '2"', '3"', '4"'
    price = Column(Float, default=0.0)
    product_families = Column(String)  # Comma-separated, e.g., "LS2000,LS6000" 