from sqlalchemy import Column, Integer, String
from src.core.database import Base

class VoltageOption(Base):
    """Model for storing available voltage options for each product family."""
    
    __tablename__ = "voltage_options"
    
    id = Column(Integer, primary_key=True)
    product_family = Column(String, nullable=False)  # e.g., "LS2000", "LS6000"
    voltage = Column(String, nullable=False)  # e.g., "24VDC", "115VAC"
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available
    
    def __repr__(self):
        return f"<VoltageOption(product_family='{self.product_family}', voltage='{self.voltage}')>" 