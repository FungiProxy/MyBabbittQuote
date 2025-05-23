"""
Main window module for the Babbitt Quote Generator application.

This module defines the main application window and its core functionality. It includes:
- Tab-based interface for product selection, specifications, quotes, and spare parts
- Navigation controls between tabs
- Quote management (save and export)
- Signal handling for inter-tab communication

The main window serves as the central hub for all quote generation activities,
coordinating between different tabs and managing the overall application state.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTabWidget, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, Slot, QTimer

from src.ui.product_tab import ProductTab
from src.ui.specifications_tab import SpecificationsTab
from src.ui.quote_tab import QuoteTab
from src.ui.spare_parts_tab import SparePartsTab

class MainWindow(QMainWindow):
    """
    Main application window for the Babbitt Quote Generator.
    
    This window serves as the primary interface for the quote generation system,
    providing a tabbed interface for product selection, specifications configuration,
    quote management, and spare parts selection.
    
    The window manages navigation between tabs, coordinates communication between
    different components, and handles quote saving and export functionality.
    
    Attributes:
        central_widget (QWidget): Main container widget
        main_layout (QVBoxLayout): Primary layout manager
        tabs (QTabWidget): Tab container for different sections
        product_tab (ProductTab): Tab for product selection
        specifications_tab (SpecificationsTab): Tab for product specifications
        quote_tab (QuoteTab): Tab for quote management
        spare_parts_tab (SparePartsTab): Tab for spare parts selection
        prev_button (QPushButton): Navigation button for previous tab
        next_button (QPushButton): Navigation button for next tab
        save_button (QPushButton): Button to save current quote
        export_button (QPushButton): Button to export quote as PDF
    
    Signals Handled:
        product_selected: Emitted when a product is selected
        specs_updated: Emitted when specifications are modified
        specs_add_to_quote: Emitted when specs should be added to quote
        part_selected: Emitted when a spare part is selected
    """
    
    def __init__(self):
        """Initialize the main window and set up the UI components."""
        super().__init__()
        self.setWindowTitle("Babbitt Quote Generator")
        self.resize(1000, 800)
        
        # Print debug info
        print("MainWindow.__init__() called")
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create tabs for different sections
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Create tabs for each section
        print("Creating ProductTab...")
        self.product_tab = ProductTab()
        print("Creating SpecificationsTab...")
        self.specifications_tab = SpecificationsTab()
        print("Creating QuoteTab...")
        self.quote_tab = QuoteTab()
        print("Creating SparePartsTab...")
        self.spare_parts_tab = SparePartsTab()
        
        self.tabs.addTab(self.product_tab, "Product Selection")
        self.tabs.addTab(self.specifications_tab, "Specifications")
        self.tabs.addTab(self.quote_tab, "Quote Summary")
        self.tabs.addTab(self.spare_parts_tab, "Spare Parts")
        
        # Bottom buttons for navigation and actions
        self.button_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.save_button = QPushButton("Save Quote")
        self.export_button = QPushButton("Export PDF")
        
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)
        self.button_layout.addStretch()  # Add spacer to push save/export buttons to the right
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.export_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # Connect tab signals
        print("Connecting signals...")
        self._connect_signals()
        
        # Apply initial button states
        self.update_button_states()
        
        # Add a timer to check window state
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_window_state)
        self.check_timer.start(1000)  # Check every second
        
        print("MainWindow initialization complete")
    
    def showEvent(self, event):
        """Called when the window is shown."""
        super().showEvent(event)
        print(f"Window shown: Geometry = {self.geometry().x()}, {self.geometry().y()}, {self.geometry().width()}, {self.geometry().height()}")
        print(f"Window visible: {self.isVisible()}")
        print(f"Window active: {self.isActiveWindow()}")
    
    def check_window_state(self):
        """Check the window state and print debug info."""
        print(f"Window check: Visible={self.isVisible()}, Active={self.isActiveWindow()}, Minimized={self.isMinimized()}")
        # Stop the timer after a few checks
        if hasattr(self, 'check_count'):
            self.check_count += 1
            if self.check_count > 5:
                self.check_timer.stop()
        else:
            self.check_count = 1
    
    def _connect_signals(self):
        """
        Connect all signal handlers for the main window.
        
        Sets up connections between:
        - Tab signals (product selection, specs updates, etc.)
        - Button click handlers
        - Tab change events
        """
        # Tab signals
        self.product_tab.product_selected.connect(self.on_product_selected)
        self.specifications_tab.specs_updated.connect(self.on_specs_updated)
        self.specifications_tab.add_to_quote.connect(self.on_specs_add_to_quote)
        self.spare_parts_tab.part_selected.connect(self.on_spare_part_selected)
        
        # Button signals
        self.next_button.clicked.connect(self.next_tab)
        self.prev_button.clicked.connect(self.prev_tab)
        self.save_button.clicked.connect(self.save_quote)
        self.export_button.clicked.connect(self.export_quote)
        self.tabs.currentChanged.connect(self.on_tab_changed)
    
    @Slot(str)
    def on_product_selected(self, model):
        """
        Handle product selection events.
        
        Updates the specifications and quote tabs with the newly selected product
        information.
        
        Args:
            model (str): The model number/identifier of the selected product
        """
        print(f"Product selected: {model}")
        # Get full product info including derived category
        product_info = self.product_tab.get_selected_product()
        category = product_info["category"]
        
        # Update specifications tab with product info
        self.specifications_tab.update_for_product(category, model)
        
        # Update quote tab with product info
        self.quote_tab.update_product_info(product_info)
    
    def on_specs_updated(self, specs):
        """
        Handle specification update events.
        
        Updates the quote tab with the modified specifications.
        
        Args:
            specs (dict): Dictionary containing the updated specifications
        """
        print("Specifications updated")
        # Update quote tab with specifications
        self.quote_tab.update_specifications(specs)
    
    def update_button_states(self):
        """
        Update the enabled/disabled state of navigation buttons.
        
        Enables/disables the Previous and Next buttons based on the current
        tab index and total number of tabs.
        """
        current_index = self.tabs.currentIndex()
        
        # Enable/disable previous button
        self.prev_button.setEnabled(current_index > 0)
        
        # Enable/disable next button
        self.next_button.setEnabled(current_index < self.tabs.count() - 1)
    
    def on_tab_changed(self, index):
        """
        Handle tab change events.
        
        Updates button states when the active tab changes.
        
        Args:
            index (int): Index of the newly selected tab
        """
        print(f"Tab changed to: {index}")
        self.update_button_states()
    
    @Slot()
    def next_tab(self):
        """Navigate to the next tab if available."""
        current = self.tabs.currentIndex()
        if current < self.tabs.count() - 1:
            self.tabs.setCurrentIndex(current + 1)
    
    @Slot()
    def prev_tab(self):
        """Navigate to the previous tab if available."""
        current = self.tabs.currentIndex()
        if current > 0:
            self.tabs.setCurrentIndex(current - 1)
    
    @Slot()
    def save_quote(self):
        """
        Save the current quote.
        
        Validates that a product is selected and saves the quote data.
        Currently shows a success message; in production, this would
        save to a database.
        
        Raises:
            QMessageBox: Warning if no product is selected
        """
        print("Save quote action triggered")
        # Get quote data
        quote_data = self.quote_tab.get_quote_data()
        
        # Check if product is selected
        if not quote_data['product'].get('model'):
            QMessageBox.warning(self, "Missing Product", 
                "Please select a product before saving the quote.")
            return
        
        # In the full implementation, this would save to your database
        # For now, we'll just show a success message
        customer_name = quote_data['customer'].get('name', 'Customer')
        product_model = quote_data['product'].get('model', 'Unknown')
        
        QMessageBox.information(self, "Quote Saved", 
            f"Quote for {customer_name} for {product_model} has been saved.")
    
    @Slot()
    def export_quote(self):
        """
        Export the current quote to PDF.
        
        Validates that a product is selected, prompts for save location,
        and exports the quote. Currently shows a success message; in
        production, this would generate a PDF.
        
        Raises:
            QMessageBox: Warning if no product is selected
        """
        print("Export quote action triggered")
        # Get quote data
        quote_data = self.quote_tab.get_quote_data()
        
        # Check if product is selected
        if not quote_data['product'].get('model'):
            QMessageBox.warning(self, "Missing Product", 
                "Please select a product before exporting the quote.")
            return
        
        # Get file path from user
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Quote", "", "PDF Files (*.pdf)")
        
        if not file_path:
            return  # User cancelled
            
        if not file_path.lower().endswith('.pdf'):
            file_path += '.pdf'
        
        # In the full implementation, this would call your PDF export functionality
        # For now, we'll just show a success message
        QMessageBox.information(self, "Export PDF", 
            f"Quote has been exported to {file_path}")
    
    @Slot(dict)
    def on_spare_part_selected(self, part_info):
        """
        Handle spare part selection events.
        
        Adds the selected spare part to the quote and switches to the quote tab.
        
        Args:
            part_info (dict): Dictionary containing spare part information
        """
        print(f"Spare part selected: {part_info['part_number']}")
        
        # Add the spare part to the quote
        self.quote_tab.add_spare_part_to_quote(part_info)
        
        # Switch to quote tab to see the added part
        self.tabs.setCurrentWidget(self.quote_tab)
    
    @Slot(dict)
    def on_specs_add_to_quote(self, specs):
        """
        Handle adding specifications to the quote.
        
        Validates product selection, adds the configured product to the quote,
        and switches to the quote tab.
        
        Args:
            specs (dict): Dictionary containing product specifications
        
        Raises:
            QMessageBox: Warning if no product is selected
        """
        print("Adding specifications to quote")
        
        # Get the current product info
        product_info = self.product_tab.get_selected_product()
        
        # Create a description for the quote item
        if product_info and product_info.get("model"):
            # Add the current product and specs to the quote items
            self._add_product_to_quote_items(product_info, specs)
            
            # Show success message to user
            QMessageBox.information(self, "Added to Quote", 
                f"{product_info.get('model')} has been added to your quote.")
            
            # Switch to the Quote tab
            self.tabs.setCurrentWidget(self.quote_tab)
        else:
            QMessageBox.warning(self, "No Product Selected", 
                "Please select a product before adding to quote.")
    
    def _add_product_to_quote_items(self, product_info, specs):
        """
        Add a product to the quote items.
        
        Internal helper method to add a product configuration to the quote.
        
        Args:
            product_info (dict): Dictionary containing product information
            specs (dict): Dictionary containing product specifications
        """
        # Calculate price based on specs
        base_price = 0.0
        options_price = 0.0
        
        # This would normally be done in a proper pricing module
        model = product_info.get("model", "")
        base_model = model.split()[0] if model else ""
        
        # Set base prices for each model (simplified example)
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
        base_price = model_prices.get(base_model, 0.0)
        
        # This is a simplified version - in a real app, you'd have more sophisticated pricing
        # Call the appropriate method in the quote tab to add this product
        item_info = {
            "type": "product",
            "id": base_model,
            "name": model,
            "description": f"{model} - {product_info.get('category', '')}",
            "price": base_price + options_price,
            "specifications": specs
        }
        
        # Add to quote items table
        self.quote_tab.add_spare_part_to_quote(item_info)
    
    def setup_styles(self):
        """Apply stylesheets for a clean UI."""
        print("Applying styles...")
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #F5F5F9;
                color: #050D10;
                font-family: Arial, sans-serif;
            }
            
            QGroupBox {
                border: 1px solid #99AEBD;
                border-radius: 5px;
                margin-top: 1em;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            
            QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit {
                border: 1px solid #99AEBD;
                border-radius: 3px;
                padding: 5px;
                background-color: white;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #71988C;
                height: 10px;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #08D13F;
                border: 1px solid #5c5c5c;
                width: 18px;
                border-radius: 9px;
                margin: -5px 0;
            }
            
            QPushButton {
                background-color: #71988C;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #08D13F;
            }
            
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
            
            #export_button {
                background-color: #08D13F;
            }
            
            #export_button:hover {
                background-color: #05A32F;
            }
            
            QTabWidget::pane {
                border: 1px solid #99AEBD;
                border-radius: 5px;
            }
            
            QTabBar::tab {
                background-color: #99AEBD;
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: #71988C;
            }
            
            QTableWidget {
                border: 1px solid #99AEBD;
                gridline-color: #DDDDDD;
            }
            
            QTableWidget::item {
                padding: 4px;
            }
            
            QHeaderView::section {
                background-color: #71988C;
                color: white;
                padding: 4px;
                border: 1px solid #99AEBD;
            }
        """)
        
        # Set object names for styling
        self.export_button.setObjectName("export_button")
        print("Styles applied successfully") 