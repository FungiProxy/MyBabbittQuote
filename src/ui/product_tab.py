"""
Product Selection Tab for the Babbitt Quote Generator
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QGroupBox, QFormLayout, QSpacerItem,
    QSizePolicy
)
from PySide6.QtCore import Signal


class ProductTab(QWidget):
    """Product selection tab for the quote generator."""
    
    # Signals
    product_selected = Signal(str, str)  # category, model
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
        # Connect signals
        self.product_category.currentIndexChanged.connect(self.on_category_changed)
        self.product_model.currentIndexChanged.connect(self.on_model_changed)
        
    def init_ui(self):
        """Initialize the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Product category selection
        self.category_group = QGroupBox("Product Category")
        category_layout = QFormLayout()
        
        self.product_category = QComboBox()
        # Initially, we'll add placeholder categories
        # These would later be populated from ProductService
        self.product_category.addItems([
            "Point Level Switches",
            "Continuous Measurement Transmitters",
            "Multi-Point Level Switches",
            "Magnetic Level Indicators",
            "Dust Emissions Monitors"
        ])
        
        category_layout.addRow("Select Product Category:", self.product_category)
        self.category_group.setLayout(category_layout)
        
        # Product model selection
        self.model_group = QGroupBox("Product Model")
        model_layout = QFormLayout()
        
        self.product_model = QComboBox()
        # Initially empty - will be populated based on category selection
        
        model_layout.addRow("Select Product Model:", self.product_model)
        self.model_group.setLayout(model_layout)
        
        # Application selection
        self.application_group = QGroupBox("Application")
        application_layout = QFormLayout()
        
        self.application_type = QComboBox()
        self.application_type.addItems([
            "Oil & Gas",
            "Refining",
            "Petrochemical",
            "Water/Wastewater",
            "Food Processing",
            "Dry Bulk Solid"
        ])
        
        application_layout.addRow("Industry Application:", self.application_type)
        self.application_group.setLayout(application_layout)
        
        # Add everything to main layout
        main_layout.addWidget(self.category_group)
        main_layout.addWidget(self.model_group)
        main_layout.addWidget(self.application_group)
        
        # Add product info section (will be populated dynamically)
        self.info_group = QGroupBox("Product Information")
        info_layout = QVBoxLayout()
        self.product_info_label = QLabel("Select a product to view details")
        info_layout.addWidget(self.product_info_label)
        self.info_group.setLayout(info_layout)
        
        main_layout.addWidget(self.info_group)
        
        # Add a spacer at the bottom to push everything up
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def on_category_changed(self, index):
        """Handle category selection changes."""
        self.product_model.clear()
        
        # This would normally fetch from ProductService
        # For now, we'll add placeholder models based on the category
        if index == 0:  # Point Level Switches
            models = ["RF Admittance", "Capacitance", "Vibration"]
        elif index == 1:  # Continuous Measurement
            models = ["Ultrasonic", "Radar", "Guided Wave Radar"]
        elif index == 2:  # Multi-Point Level Switches
            models = ["Float Type", "Magnetostrictive", "Resistive Chain"]
        elif index == 3:  # Magnetic Level Indicators
            models = ["Standard", "High Pressure", "High Temperature"]
        else:  # Dust Emissions Monitors
            models = ["Particulate Monitor", "Broken Bag Detector"]
        
        self.product_model.addItems(models)
    
    def on_model_changed(self, index):
        """Handle model selection changes."""
        if index >= 0:
            category = self.product_category.currentText()
            model = self.product_model.currentText()
            
            # Update product info
            self.update_product_info(category, model)
            
            # Emit signal with selected product
            self.product_selected.emit(category, model)
    
    def update_product_info(self, category, model):
        """Update the product information section."""
        # This would normally fetch detailed product info from ProductService
        # For now, we'll just display the selection
        info_text = f"<h3>{model}</h3>"
        info_text += f"<p><b>Category:</b> {category}</p>"
        info_text += "<p>This is a placeholder for detailed product information. In the full implementation, this would show product descriptions, features, and specifications overview.</p>"
        
        self.product_info_label.setText(info_text)
    
    def get_selected_product(self):
        """Get the currently selected product information."""
        return {
            "category": self.product_category.currentText(),
            "model": self.product_model.currentText(),
            "application": self.application_type.currentText()
        }
        
    def connect_service(self, product_service):
        """Connect this tab to the product service."""
        # This would be implemented to fetch real data from your service
        pass 