"""
Pricing module for calculating product prices with complex rules.
"""
from typing import Optional

from sqlalchemy.orm import Session

from src.core.models import Material, ProductVariant, StandardLength


def calculate_product_price(
    db: Session, 
    product_id: int, 
    length: Optional[float] = None,
    material_override: Optional[str] = None
) -> float:
    """
    Calculate the price of a product with the given configuration.
    
    Args:
        db: Database session
        product_id: ID of the product variant
        length: Length in inches (if applicable)
        material_override: Material code to override the product's default material
        
    Returns:
        Calculated price
    """
    # Get product variant
    product = db.query(ProductVariant).filter(ProductVariant.id == product_id).first()
    if not product:
        raise ValueError(f"Product with ID {product_id} not found")
    
    # If no length specified, use the base length
    if length is None:
        length = product.base_length
    
    # Determine material to use
    material_code = material_override if material_override else product.material
    
    # Get material information
    material = db.query(Material).filter(Material.code == material_code).first()
    if not material:
        raise ValueError(f"Material {material_code} not found")
    
    # Start with base price
    price = product.base_price
    
    # If material is different from product's default, adjust base price
    if material_override and material_override != product.material:
        # For U and T materials, calculate based on S material price
        s_material_product = db.query(ProductVariant).filter(
            ProductVariant.product_family_id == product.product_family_id,
            ProductVariant.voltage == product.voltage,
            ProductVariant.material == "S"
        ).first()
        
        if s_material_product and material.base_price_adder:
            # Start with S material price and add the material-specific adder
            price = s_material_product.base_price + material.base_price_adder
    
    # Calculate price for length beyond base length
    if length > material.base_length:
        extra_length = length - material.base_length
        
        if material.length_adder_per_inch:
            # Price per inch
            price += extra_length * material.length_adder_per_inch
        elif material.length_adder_per_foot:
            # Price per foot (convert inches to feet)
            price += (extra_length / 12) * material.length_adder_per_foot
    
    # Apply non-standard length surcharge if applicable
    if material.has_nonstandard_length_surcharge:
        # Check if length is a standard length
        is_standard = db.query(StandardLength).filter(
            StandardLength.material_code == material_code,
            StandardLength.length == length
        ).first() is not None
        
        if not is_standard:
            price += material.nonstandard_length_surcharge
    
    return price


def calculate_option_price(option_price: float, option_price_type: str, length: Optional[float] = None) -> float:
    """
    Calculate the price of an option based on its type and parameters.
    
    Args:
        option_price: Base price of the option
        option_price_type: Type of pricing ("fixed", "per_inch", "per_foot")
        length: Length in inches (required for per_inch and per_foot options)
        
    Returns:
        Calculated option price
    """
    if option_price_type == "fixed":
        return option_price
    elif option_price_type == "per_inch" and length is not None:
        return option_price * length
    elif option_price_type == "per_foot" and length is not None:
        # Convert inches to feet
        return option_price * (length / 12)
    else:
        return option_price  # Default to fixed price 