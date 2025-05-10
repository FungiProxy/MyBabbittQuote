from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTabWidget, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, Slot, QTimer

from src.ui.product_tab import ProductTab
from src.ui.specifications_tab import SpecificationsTab
from src.ui.quote_tab import QuoteTab

class MainWindow(QMainWindow):
    """Main application window for the Babbitt Quote Generator."""
    
    def __init__(self):
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
        
        self.tabs.addTab(self.product_tab, "Product Selection")
        self.tabs.addTab(self.specifications_tab, "Specifications")
        self.tabs.addTab(self.quote_tab, "Quote Summary")
        
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
        self.product_tab.product_selected.connect(self.on_product_selected)
        self.specifications_tab.specs_updated.connect(self.on_specs_updated)
        
        # Connect button signals
        self.next_button.clicked.connect(self.next_tab)
        self.prev_button.clicked.connect(self.prev_tab)
        self.save_button.clicked.connect(self.save_quote)
        self.export_button.clicked.connect(self.export_quote)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
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
    
    def on_product_selected(self, category, model):
        """Handle product selection."""
        print(f"Product selected: {category} - {model}")
        # Update specifications tab with product info
        self.specifications_tab.update_for_product(category, model)
        
        # Update quote tab with product info
        product_info = self.product_tab.get_selected_product()
        self.quote_tab.update_product_info(product_info)
    
    def on_specs_updated(self, specs):
        """Handle specifications updates."""
        print("Specifications updated")
        # Update quote tab with specifications
        self.quote_tab.update_specifications(specs)
    
    def update_button_states(self):
        """Update navigation button states based on current tab."""
        current_index = self.tabs.currentIndex()
        
        # Enable/disable previous button
        self.prev_button.setEnabled(current_index > 0)
        
        # Enable/disable next button
        self.next_button.setEnabled(current_index < self.tabs.count() - 1)
    
    def on_tab_changed(self, index):
        """Handle tab changes."""
        print(f"Tab changed to: {index}")
        self.update_button_states()
    
    @Slot()
    def next_tab(self):
        """Navigate to the next tab."""
        current = self.tabs.currentIndex()
        if current < self.tabs.count() - 1:
            self.tabs.setCurrentIndex(current + 1)
    
    @Slot()
    def prev_tab(self):
        """Navigate to the previous tab."""
        current = self.tabs.currentIndex()
        if current > 0:
            self.tabs.setCurrentIndex(current - 1)
    
    @Slot()
    def save_quote(self):
        """Save the current quote."""
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
        """Export the current quote to PDF."""
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