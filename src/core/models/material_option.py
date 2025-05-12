from sqlalchemy import Column, Integer, String, Float
from src.core.database import Base

class MaterialOption(Base):
    """Model for storing available material options for each product family."""
    
    __tablename__ = "material_options"
    
    id = Column(Integer, primary_key=True)
    product_family = Column(String, nullable=False)  # e.g., "LS2000", "LS6000"
    material_code = Column(String, nullable=False)  # e.g., "S", "H", "A"
    display_name = Column(String, nullable=False)  # e.g., "S - 316 Stainless Steel"
    base_price = Column(Float, default=0.0)  # Additional cost for this material
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available
    
    def __repr__(self):
        return f"<MaterialOption(product_family='{self.product_family}', material='{self.material_code}', display_name='{self.display_name}')>" 