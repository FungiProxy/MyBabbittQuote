"""
Test the pricing module.

This script tests the pricing calculations for various product configurations.
"""
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.core.models import ProductVariant, Material
from src.core.pricing import calculate_product_price, calculate_option_price


def test_product_pricing(db: Session):
    """Test product price calculations for various configurations."""
    # Get product variants
    variants = db.query(ProductVariant).all()
    
    if not variants:
        print("No product variants found. Please populate the database first.")
        return
    
    print("\n=== Product Pricing Tests ===\n")
    
    # Test standard product pricing
    for variant in variants:
        price = calculate_product_price(db, variant.id)
        print(f"{variant.model_number} (Base): ${price:.2f}")
        
        # Test with longer length
        if variant.base_length:
            longer_length = variant.base_length + 10
            price = calculate_product_price(db, variant.id, longer_length)
            print(f"{variant.model_number} (Length {longer_length}\"): ${price:.2f}")
    
    # Test with material override
    # First get a variant with "S" material to test material overrides
    s_variant = db.query(ProductVariant).filter(ProductVariant.material == "S").first()
    if s_variant:
        print(f"\nMaterial override tests using {s_variant.model_number}:")
        # Try different materials
        materials = db.query(Material).all()
        for material in materials:
            if material.code != s_variant.material:
                try:
                    price = calculate_product_price(db, s_variant.id, material_override=material.code)
                    print(f"  Material {material.code}: ${price:.2f}")
                except Exception as e:
                    print(f"  Material {material.code}: Error - {str(e)}")


def test_option_pricing():
    """Test option price calculations."""
    print("\n=== Option Pricing Tests ===\n")
    
    # Test fixed price options
    price = calculate_option_price(40.0, "fixed")
    print(f"Fixed price option ($40.00): ${price:.2f}")
    
    # Test per_inch options
    price = calculate_option_price(10.0, "per_inch", 20.0)
    print(f"Per-inch option ($10.00/inch × 20\"): ${price:.2f}")
    
    # Test per_foot options
    price = calculate_option_price(30.0, "per_foot", 24.0)
    print(f"Per-foot option ($30.00/foot × 24\" = 2ft): ${price:.2f}")


def main():
    """Run pricing module tests."""
    db = SessionLocal()
    
    try:
        test_product_pricing(db)
        test_option_pricing()
        
        print("\nPricing tests complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main() 