"""
Pricing module for calculating product prices with complex rules.
"""
from typing import Optional

from sqlalchemy.orm import Session

from src.core.models import Material, Product, StandardLength, MaterialAvailability


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
        product_id: ID of the product
        length: Length in inches (if applicable)
        material_override: Material code to override the product's default material
        
    Returns:
        Calculated price
        
    Raises:
        ValueError: If the product doesn't exist, the material doesn't exist, or the material
                   is not available for the product
    """
    # Get product
    product = db.query(Product).filter(Product.id == product_id).first()
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
    
    # Check if the material is available for this product type
    if material_override:
        # Extract the base product type (e.g., "LS2000" from "LS2000-115VAC-S-10")
        product_type = product.model_number.split('-')[0]
        
        # Special handling for dual point switches which have a format like "LS7000/2-115VAC-H-10"
        if "/" in product_type:
            product_type = product_type.split("/")[0] + "/" + product_type.split("/")[1]
        
        # Check if the material is available for this product type
        availability = db.query(MaterialAvailability).filter(
            MaterialAvailability.material_code == material_code,
            MaterialAvailability.product_type == product_type,
            MaterialAvailability.is_available == True
        ).first()
        
        if not availability:
            raise ValueError(f"Material {material_code} is not available for product type {product_type}")
    
    # Start with base price
    price = product.base_price
    
    # Material price adjustments
    if material_override and material_override != product.material:
        # For exotic materials (U and T), calculate based on S material price
        if material_override in ['U', 'T']:  # U = UHMWPE, T = Teflon
            s_material_product = db.query(Product).filter(
                Product.model_number == product.model_number,
                Product.voltage == product.voltage,
                Product.material == "S"  # S = 316 Stainless Steel
            ).first()
            
            if s_material_product:
                # Start with S material price
                price = s_material_product.base_price
                
                # Add material-specific premium based on additional_info.txt
                if material_override == 'U':  # UHMWPE
                    price += 20.0  # $20 adder to S base price
                elif material_override == 'T':  # Teflon
                    price += 60.0  # $60 adder to S base price
        elif material_override == 'H':  # H = Halar Coated
            # No base price adjustment for Halar Coated in additional_info.txt
            pass
    
    # Length price adjustments
    if length and length > product.base_length:
        extra_length = length - product.base_length
        
        # Apply material-specific length adders based on additional_info.txt
        if material_code == 'S':
            # $45/foot = $3.75/inch
            price += extra_length * 3.75
        elif material_code == 'H' or material_code == 'TS':
            # $110/foot = $9.17/inch
            price += extra_length * 9.17
        elif material_code == 'U':
            # $40/inch
            price += extra_length * 40.0
        elif material_code == 'T':
            # $50/inch
            price += extra_length * 50.0
    
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


def calculate_option_price(
    option_price: float,
    option_price_type: str,
    length: Optional[float] = None
) -> float:
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