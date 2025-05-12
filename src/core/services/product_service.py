"""
Service for managing products and product configuration.
"""
from typing import List, Optional, Dict, Any, Tuple

from sqlalchemy.orm import Session

from src.core.models import Product, Material, Option, MaterialAvailability, VoltageOption, MaterialOption
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
    def get_available_voltages(db: Session, product_family: str) -> List[str]:
        """
        Get available voltages for a product family.
        
        Args:
            db: Database session
            product_family: Product family code (e.g., "LS2000", "LS7000")
            
        Returns:
            List of available voltage options
        """
        voltages = db.query(VoltageOption).filter(
            VoltageOption.product_family == product_family,
            VoltageOption.is_available == 1
        ).all()
        
        return [v.voltage for v in voltages]
    
    @staticmethod
    def get_available_materials_for_product(db: Session, product_family: str) -> List[Dict[str, Any]]:
        """
        Get available materials for a product family.
        
        Args:
            db: Database session
            product_family: Product family code (e.g., "LS2000", "LS7000")
            
        Returns:
            List of dictionaries containing material information
        """
        materials = db.query(MaterialOption).filter(
            MaterialOption.product_family == product_family,
            MaterialOption.is_available == 1
        ).all()
        
        return [
            {
                'code': m.material_code,
                'display_name': m.display_name,
                'base_price': m.base_price
            }
            for m in materials
        ]
    
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