"""
Service for managing products and product configuration.
"""
from typing import List, Optional, Dict, Any, Tuple

from sqlalchemy.orm import Session

from src.core.models import ProductFamily, ProductVariant, Material, Option
from src.core.pricing import calculate_product_price
from src.utils.db_utils import get_by_id, get_all


class ProductService:
    """Service for managing products and product configuration."""
    
    @staticmethod
    def get_product_families(db: Session) -> List[ProductFamily]:
        """
        Get all product families.
        
        Args:
            db: Database session
            
        Returns:
            List of all ProductFamily objects
        """
        return get_all(db, ProductFamily)
    
    @staticmethod
    def get_product_variants(
        db: Session,
        family_id: Optional[int] = None,
        material: Optional[str] = None,
        voltage: Optional[str] = None
    ) -> List[ProductVariant]:
        """
        Get product variants, optionally filtered by family, material, or voltage.
        
        Args:
            db: Database session
            family_id: Optional product family ID to filter by
            material: Optional material code to filter by
            voltage: Optional voltage to filter by
            
        Returns:
            List of matching ProductVariant objects
        """
        query = db.query(ProductVariant)
        
        if family_id is not None:
            query = query.filter(ProductVariant.product_family_id == family_id)
        
        if material is not None:
            query = query.filter(ProductVariant.material == material)
            
        if voltage is not None:
            query = query.filter(ProductVariant.voltage == voltage)
            
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
    def get_product_options(
        db: Session,
        product_family_id: Optional[int] = None
    ) -> List[Option]:
        """
        Get available options, optionally filtered by product family.
        
        Args:
            db: Database session
            product_family_id: Optional product family ID to filter by
            
        Returns:
            List of matching Option objects
        """
        query = db.query(Option)
        
        if product_family_id is not None:
            query = query.filter(Option.product_family_id == product_family_id)
            
        return query.all()
    
    @staticmethod
    def configure_product(
        db: Session,
        product_id: int,
        length: Optional[float] = None,
        material_override: Optional[str] = None
    ) -> Tuple[ProductVariant, float]:
        """
        Configure a product with specified parameters and calculate its price.
        
        Args:
            db: Database session
            product_id: ID of the product variant
            length: Length in inches (if applicable)
            material_override: Material code to override product's default
            
        Returns:
            Tuple of (ProductVariant, calculated_price)
            
        Raises:
            ValueError: If product not found
        """
        # Get product
        product = get_by_id(db, ProductVariant, product_id)
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
    def search_products(db: Session, search_term: str) -> List[ProductVariant]:
        """
        Search for products by name, description, or model number.
        
        Args:
            db: Database session
            search_term: Search term to match against various product fields
            
        Returns:
            List of matching ProductVariant objects
        """
        search_pattern = f"%{search_term}%"
        
        # First get matching families
        family_query = db.query(ProductFamily).filter(
            (ProductFamily.name.ilike(search_pattern)) |
            (ProductFamily.description.ilike(search_pattern))
        )
        
        matching_family_ids = [family.id for family in family_query.all()]
        
        # Then query variants
        return db.query(ProductVariant).filter(
            (ProductVariant.description.ilike(search_pattern)) |
            (ProductVariant.model_number.ilike(search_pattern)) |
            (ProductVariant.product_family_id.in_(matching_family_ids))
        ).all() 