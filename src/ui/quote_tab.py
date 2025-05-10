"""
Quote Summary Tab for the Babbitt Quote Generator
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QGroupBox, QFormLayout, QSpacerItem,
    QSizePolicy, QPushButton, QTextEdit, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class QuoteTab(QWidget):
    """Quote summary tab for the quote generator."""
    
    # Signals
    customer_updated = Signal(dict)  # customer information dictionary
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
        # Initialize data structures
        self.product_info = {}
        self.specs = {}
        self.pricing = {
            "base_price": 0.0,
            "options_price": 0.0,
            "total_price": 0.0
        }
    
    def init_ui(self):
        """Initialize the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create summary section
        summary_group = QGroupBox("Quote Summary")
        summary_layout = QVBoxLayout()
        
        # Product summary
        self.product_summary = QLabel("No product selected")
        self.product_summary.setStyleSheet("font-weight: bold;")
        summary_layout.addWidget(self.product_summary)
        
        # Specifications summary
        self.specs_table = QTableWidget(0, 2)
        self.specs_table.setHorizontalHeaderLabels(["Specification", "Value"])
        self.specs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.specs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.specs_table.verticalHeader().setVisible(False)
        summary_layout.addWidget(self.specs_table)
        
        summary_group.setLayout(summary_layout)
        main_layout.addWidget(summary_group)
        
        # Create pricing section
        pricing_group = QGroupBox("Pricing")
        pricing_layout = QFormLayout()
        
        self.base_price_label = QLabel("$0.00")
        pricing_layout.addRow("Base Price:", self.base_price_label)
        
        self.options_price_label = QLabel("$0.00")
        pricing_layout.addRow("Options:", self.options_price_label)
        
        self.total_price_label = QLabel("$0.00")
        font = QFont()
        font.setBold(True)
        self.total_price_label.setFont(font)
        pricing_layout.addRow("Total Price:", self.total_price_label)
        
        pricing_group.setLayout(pricing_layout)
        main_layout.addWidget(pricing_group)
        
        # Create customer information section
        customer_group = QGroupBox("Customer Information")
        customer_layout = QFormLayout()
        
        self.customer_name = QLineEdit()
        customer_layout.addRow("Customer Name:", self.customer_name)
        
        self.contact_name = QLineEdit()
        customer_layout.addRow("Contact Person:", self.contact_name)
        
        self.email = QLineEdit()
        customer_layout.addRow("Email:", self.email)
        
        self.phone = QLineEdit()
        customer_layout.addRow("Phone:", self.phone)
        
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(100)
        customer_layout.addRow("Notes:", self.notes)
        
        customer_group.setLayout(customer_layout)
        main_layout.addWidget(customer_group)
        
        # Connect signals
        self.customer_name.textChanged.connect(self.on_customer_info_changed)
        self.contact_name.textChanged.connect(self.on_customer_info_changed)
        self.email.textChanged.connect(self.on_customer_info_changed)
        self.phone.textChanged.connect(self.on_customer_info_changed)
        self.notes.textChanged.connect(self.on_customer_info_changed)
        
        # Add spacer
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def update_product_info(self, product_info):
        """Update product information."""
        self.product_info = product_info
        
        # Update product summary label
        category = product_info.get("category", "")
        model = product_info.get("model", "")
        application = product_info.get("application", "")
        
        if category and model:
            self.product_summary.setText(f"<b>{model}</b> ({category})<br>Application: {application}")
        else:
            self.product_summary.setText("No product selected")
        
        # Update pricing (this would normally be calculated by your pricing module)
        self.update_pricing()
    
    def update_specifications(self, specs):
        """Update specifications summary."""
        self.specs = specs
        
        # Clear existing specs
        self.specs_table.setRowCount(0)
        
        # Add specs to table
        row = 0
        for name, value in specs.items():
            # Convert internal name to display name
            display_name = name.replace("_", " ").title()
            
            # Format value for display
            if isinstance(value, bool):
                display_value = "Yes" if value else "No"
            else:
                display_value = str(value)
            
            # Add to table
            self.specs_table.insertRow(row)
            self.specs_table.setItem(row, 0, QTableWidgetItem(display_name))
            self.specs_table.setItem(row, 1, QTableWidgetItem(display_value))
            row += 1
        
        # Update pricing (this would normally be calculated by your pricing module)
        self.update_pricing()
    
    def update_pricing(self):
        """Update pricing based on product and specifications."""
        # This would normally call your pricing.py module
        # For now, we'll use placeholder calculations
        
        # Base price based on product
        base_price = 0.0
        if "Point Level" in self.product_info.get("category", ""):
            base_price = 800.0
        elif "Continuous" in self.product_info.get("category", ""):
            base_price = 1200.0
        elif "Multi-Point" in self.product_info.get("category", ""):
            base_price = 1500.0
        elif "Magnetic" in self.product_info.get("category", ""):
            base_price = 950.0
        elif "Dust" in self.product_info.get("category", ""):
            base_price = 1800.0
        
        # Options price based on specifications
        options_price = 0.0
        
        # Add costs for each option
        for name, value in self.specs.items():
            if name == "explosion_proof" and value:
                options_price += 350.0
            elif name == "high_temp" and value:
                options_price += 250.0
            elif name == "extended_probe" and value:
                options_price += 100.0
            elif name == "probe_length" and isinstance(value, (int, float)):
                # Add cost for longer probes
                if value > 24:
                    options_price += (value - 24) * 10  # $10 per inch over 24"
            
            # Add more pricing rules as needed
        
        # Calculate total
        total_price = base_price + options_price
        
        # Update pricing data
        self.pricing = {
            "base_price": base_price,
            "options_price": options_price,
            "total_price": total_price
        }
        
        # Update the UI
        self.base_price_label.setText(f"${base_price:.2f}")
        self.options_price_label.setText(f"${options_price:.2f}")
        self.total_price_label.setText(f"${total_price:.2f}")
    
    def on_customer_info_changed(self):
        """Handle changes to customer information."""
        customer_info = self.get_customer_info()
        self.customer_updated.emit(customer_info)
    
    def get_customer_info(self):
        """Get customer information from form."""
        return {
            "name": self.customer_name.text(),
            "contact": self.contact_name.text(),
            "email": self.email.text(),
            "phone": self.phone.text(),
            "notes": self.notes.toPlainText()
        }
    
    def get_quote_data(self):
        """Get all quote data for saving or exporting."""
        return {
            "product": self.product_info,
            "specifications": self.specs,
            "pricing": self.pricing,
            "customer": self.get_customer_info()
        } 