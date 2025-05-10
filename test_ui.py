#!/usr/bin/env python3
"""
Simple test script to verify UI is working
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

def main():
    """Test basic PySide6 functionality"""
    # Create application
    app = QApplication(sys.argv)
    
    # Create a simple window
    window = QMainWindow()
    window.setWindowTitle("PySide6 Test")
    window.resize(400, 300)
    
    # Create central widget
    central = QWidget()
    window.setCentralWidget(central)
    
    # Create layout
    layout = QVBoxLayout(central)
    
    # Add a label
    label = QLabel("If you can see this, PySide6 is working correctly!")
    label.setStyleSheet("font-size: 16px; color: green;")
    layout.addWidget(label)
    
    # Show window
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 