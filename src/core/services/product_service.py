"""
Service for managing products and product configuration.
"""
from typing import List, Optional, Dict, Any, Tuple

from sqlalchemy.orm import Session

from src.core.models import Product, Material, Option, MaterialAvailability
from src.core.pricing import calculate_product_price
from src.utils.db_utils import get_by_id, get_all


class ProductService:
    """Service for managing products and product configuration."""
    
    @staticmethod
    def get_products(
        db: Session,
        material: Optional[str] = None,
        voltage: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Product]:
        """
        Get products, optionally filtered by material, voltage, or category.
        
        Args:
            db: Database session
            material: Optional material code to filter by
            voltage: Optional voltage to filter by
            category: Optional category to filter by
            
        Returns:
            List of matching Product objects
        """
        query = db.query(Product)
        
        if material is not None:
            query = query.filter(Product.material == material)
            
        if voltage is not None:
            query = query.filter(Product.voltage == voltage)
            
        if category is not None:
            query = query.filter(Product.category == category)
            
        return query.all()
    
    @staticmethod
    def get_available_materials(db: Session) -> List[Material]:
        """
        Get all available materials.
        
        Args:
            db: Database session
            
        Returns:
            List of all Material objects
        """
        return get_all(db, Material)
    
    @staticmethod
    def get_available_materials_for_product(db: Session, product_type: str) -> List[Material]:
        """
        Get materials that are available for a specific product type.
        
        Args:
            db: Database session
            product_type: The product type (e.g., "LS2000", "LS7000/2")
            
        Returns:
            List of Material objects available for the product type
        """
        # Find all material codes available for this product type
        available_material_codes = db.query(MaterialAvailability.material_code).filter(
            MaterialAvailability.product_type == product_type,
            MaterialAvailability.is_available == True
        ).all()
        
        # Extract the material codes from the query results
        material_codes = [code[0] for code in available_material_codes]
        
        # Get the material objects for these codes
        if material_codes:
            materials = db.query(Material).filter(Material.code.in_(material_codes)).all()
            return materials
        return []
    
    @staticmethod
    def is_material_available_for_product(db: Session, material_code: str, product_type: str) -> bool:
        """
        Check if a specific material is available for a specific product type.
        
        Args:
            db: Database session
            material_code: The material code (e.g., "S", "H", "U")
            product_type: The product type (e.g., "LS2000", "LS7000/2")
            
        Returns:
            True if the material is available for the product type, False otherwise
        """
        availability = db.query(MaterialAvailability).filter(
            MaterialAvailability.material_code == material_code,
            MaterialAvailability.product_type == product_type
        ).first()
        
        return availability is not None and availability.is_available
    
    @staticmethod
    def get_product_options(
        db: Session,
        product_id: Optional[int] = None
    ) -> List[Option]:
        """
        Get available options, optionally filtered by product.
        
        Args:
            db: Database session
            product_id: Optional product ID to filter by
            
        Returns:
            List of matching Option objects
        """
        query = db.query(Option)
        
        if product_id is not None:
            # Get the product to check compatibility
            product = get_by_id(db, Product, product_id)
            if product and product.model_number:
                query = query.filter(
                    ~Option.excluded_products.contains(product.model_number)
                )
            
        return query.all()
    
    @staticmethod
    def configure_product(
        db: Session,
        product_id: int,
        length: Optional[float] = None,
        material_override: Optional[str] = None
    ) -> Tuple[Product, float]:
        """
        Configure a product with specified parameters and calculate its price.
        
        Args:
            db: Database session
            product_id: ID of the product
            length: Length in inches (if applicable)
            material_override: Material code to override product's default
            
        Returns:
            Tuple of (Product, calculated_price)
            
        Raises:
            ValueError: If product not found
        """
        # Get product
        product = get_by_id(db, Product, product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
            
        # Calculate price
        price = calculate_product_price(
            db=db,
            product_id=product_id,
            length=length,
            material_override=material_override
        )
        
        return product, price
        
    @staticmethod
    def search_products(db: Session, search_term: str) -> List[Product]:
        """
        Search for products by model number or description.
        
        Args:
            db: Database session
            search_term: Search term to match against product fields
            
        Returns:
            List of matching Product objects
        """
        search_pattern = f"%{search_term}%"
        
        return db.query(Product).filter(
            (Product.description.ilike(search_pattern)) |
            (Product.model_number.ilike(search_pattern))
        ).all() 