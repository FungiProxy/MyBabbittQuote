#!/usr/bin/env python3
"""
Test script to verify imports
"""

import sys
import traceback

def test_import(module_name):
    """Test importing a module and print the result"""
    print(f"Attempting to import {module_name}...")
    try:
        __import__(module_name)
        print(f"✓ Successfully imported {module_name}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import {module_name}: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"! Unexpected error importing {module_name}: {e}")
        traceback.print_exc()
        return False

def main():
    """Test all required imports"""
    print("Testing imports...\n")
    
    # Base Python imports
    print("Testing Python standard library imports:")
    test_import("os")
    test_import("sys")
    test_import("traceback")
    
    # PySide6 imports
    print("\nTesting PySide6 imports:")
    pyside = test_import("PySide6.QtWidgets")
    test_import("PySide6.QtCore")
    test_import("PySide6.QtGui")
    
    if not pyside:
        print("\nPySide6 is not properly installed. Please install it with:")
        print("pip install PySide6>=6.4.0")
        return
    
    # Our application modules
    print("\nTesting application modules:")
    test_import("src")
    test_import("src.ui")
    
    # Try to import each tab individually
    print("\nTesting individual UI modules:")
    test_import("src.ui.main_window")
    test_import("src.ui.product_tab")
    test_import("src.ui.specifications_tab")
    test_import("src.ui.quote_tab")
    
    print("\nTest complete")

if __name__ == "__main__":
    main() 