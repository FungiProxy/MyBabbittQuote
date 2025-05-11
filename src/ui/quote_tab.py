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
        
        # Configuration summary
        self.specs_table = QTableWidget(0, 2)
        self.specs_table.setHorizontalHeaderLabels(["Configuration Item", "Value"])
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
        model = product_info.get("model", "")
        application = product_info.get("application", "")
        
        if model:
            self.product_summary.setText(f"<b>{model}</b><br>Application: {application}")
        else:
            self.product_summary.setText("No product selected")
        
        # Update pricing (this would normally be calculated by your pricing module)
        self.update_pricing()
    
    def update_specifications(self, specs):
        """Update specifications summary."""
        self.specs = specs
        
        # Clear existing specs
        self.specs_table.setRowCount(0)
        
        # Group configuration items by category
        config_categories = {
            "Essential Properties": ["voltage", "material", "material_type", "viscosity"],
            "Dimensions": ["probe_length", "indicator_length", "cable_length"],
            "Connections": ["connection", "mounting"],
            "Material Options": ["exotic_metals", "oring"],
            "Housing": ["housing"],
            "Additional Features": ["high_temp", "extended_probe", "remote_display", "output_type"]
        }
        
        # Add category headers and specs in each category
        for category, spec_keys in config_categories.items():
            category_added = False
            
            for name in spec_keys:
                if name in specs:
                    # Add category header if this is the first spec in the category
                    if not category_added:
                        self._add_category_row(category)
                        category_added = True
                    
                    # Convert internal name to display name
                    display_name = name.replace("_", " ").title()
                    
                    # Format value for display
                    value = specs[name]
                    if isinstance(value, bool):
                        display_value = "Yes" if value else "No"
                    else:
                        display_value = str(value)
                    
                    # Add to table
                    self._add_spec_row(display_name, display_value)
        
        # Update pricing (this would normally be calculated by your pricing module)
        self.update_pricing()
    
    def _add_category_row(self, category_name):
        """Add a category header row to the specifications table."""
        row = self.specs_table.rowCount()
        self.specs_table.insertRow(row)
        
        category_item = QTableWidgetItem(category_name)
        category_item.setBackground(Qt.lightGray)
        category_item.setFont(QFont("", -1, QFont.Bold))
        
        # Span both columns
        self.specs_table.setItem(row, 0, category_item)
        self.specs_table.setSpan(row, 0, 1, 2)
    
    def _add_spec_row(self, name, value):
        """Add a specification row to the table."""
        row = self.specs_table.rowCount()
        self.specs_table.insertRow(row)
        
        # Add indent to name for better visual hierarchy
        name_item = QTableWidgetItem("    " + name)
        self.specs_table.setItem(row, 0, name_item)
        self.specs_table.setItem(row, 1, QTableWidgetItem(value))
    
    def update_pricing(self):
        """Update pricing based on product and specifications."""
        # This would normally call your pricing.py module
        # For now, we'll use placeholder calculations
        
        # Base price based on product model
        base_price = 0.0
        model = self.product_info.get("model", "")
        
        # Set base prices for each model
        model_prices = {
            "LS2000": 800.0,  # General Purpose
            "LS2100": 700.0,  # Loop Powered
            "LS6000": 900.0,  # Heavy Duty
            "LS7000": 1200.0, # Advanced Features
            "LS7000/2": 1500.0, # Dual Point
            "LS8000": 1100.0, # Remote Mounted
            "LS8000/2": 1400.0, # Remote Mounted Dual Point
            "LT9000": 1800.0,  # Level Transmitter
            "FS10000": 950.0   # Flow Switch
        }
        
        # Get base price for the model
        base_model = model.split()[0]  # Get just the model number without description
        base_price = model_prices.get(base_model, 0.0)
        
        # Options price based on specifications
        options_price = 0.0
        
        # Add costs for each option
        for name, value in self.specs.items():
            # Material upgrades
            if name == "material":
                if "Hastelloy" in value:
                    options_price += 400.0
                elif "Aluminum" in value:
                    options_price += 50.0
                
            # Exotic metals
            if name == "exotic_metals":
                if "Titanium" in value:
                    options_price += 600.0
                elif "Monel" in value:
                    options_price += 500.0
            
            # Special O-rings
            if name == "oring":
                if "Kalrez" in value:
                    options_price += 120.0
                elif "PTFE" in value:
                    options_price += 80.0
                elif "EPDM" in value:
                    options_price += 40.0
            
            # Housing options
            if name == "housing":
                if "Explosion-Proof" in value:
                    options_price += 300.0
                elif "Stainless Steel" in value:
                    options_price += 200.0
            
            # Feature options
            if name == "high_temp" and value:
                options_price += 150.0
            elif name == "extended_probe" and value:
                options_price += 100.0
            elif name == "remote_display" and value:
                options_price += 250.0
            
            # Output type options (for transmitters)
            if name == "output_type":
                if "HART" in value:
                    options_price += 300.0
                elif "Modbus RTU" in value:
                    options_price += 250.0
                
            # Length options
            if name == "probe_length" and isinstance(value, (int, float)):
                # Add cost for longer probes
                standard_length = 10  # Standard length is 10" for most models
                if base_model in ["LS2000", "LS2100"] and value > standard_length:
                    options_price += (value - standard_length) * 8.0  # $8 per inch over standard
                elif value > standard_length:
                    options_price += (value - standard_length) * 12.0  # $12 per inch over standard for other models
            
            if name == "cable_length" and isinstance(value, (int, float)):
                # Add cost for longer cables
                standard_cable = 10  # Standard cable length is 10 feet
                if value > standard_cable:
                    options_price += (value - standard_cable) * 5.0  # $5 per foot over standard
        
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
        customer_data = {
            "name": self.customer_name.text(),
            "contact": self.contact_name.text(),
            "email": self.email.text(),
            "phone": self.phone.text(),
            "notes": self.notes.toPlainText()
        }
        
        # Emit signal with updated customer info
        self.customer_updated.emit(customer_data)
    
    def get_quote_data(self):
        """Get all data for the current quote."""
        return {
            "product": self.product_info,
            "specifications": self.specs,
            "pricing": self.pricing,
            "customer": {
                "name": self.customer_name.text(),
                "contact": self.contact_name.text(),
                "email": self.email.text(),
                "phone": self.phone.text(),
                "notes": self.notes.toPlainText()
            }
        } 