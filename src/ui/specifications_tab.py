"""
Specifications Tab for the Babbitt Quote Generator
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QGroupBox, QFormLayout, QSpacerItem,
    QSizePolicy, QSlider, QSpinBox, QDoubleSpinBox,
    QCheckBox, QScrollArea, QLineEdit
)
from PySide6.QtCore import Qt, Signal


class SpecificationsTab(QWidget):
    """Specifications tab for the quote generator."""
    
    # Signals
    specs_updated = Signal(dict)  # specifications dictionary
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.current_product = None
        self.specs_widgets = {}  # Store references to specification widgets
        
    def init_ui(self):
        """Initialize the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create a scroll area for specifications
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.specs_layout = QVBoxLayout(self.scroll_content)
        
        # Placeholder text when no product is selected
        self.placeholder_label = QLabel(
            "Please select a product in the Product Selection tab to configure specifications."
        )
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.specs_layout.addWidget(self.placeholder_label)
        
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)
    
    def clear_specifications(self):
        """Clear all specification widgets."""
        # Remove all widgets from the layout
        while self.specs_layout.count():
            item = self.specs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear the specs widgets dictionary
        self.specs_widgets.clear()
        
        # Add placeholder back
        self.placeholder_label = QLabel(
            "Please select a product in the Product Selection tab to configure specifications."
        )
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.specs_layout.addWidget(self.placeholder_label)
    
    def update_for_product(self, category, model):
        """Update specifications based on selected product."""
        self.current_product = {"category": category, "model": model}
        
        # Clear existing specs
        self.clear_specifications()
        
        # In a real implementation, this would fetch specifications from your service
        # For now, we'll create some example specifications based on the product
        
        # Remove placeholder
        if self.placeholder_label:
            self.placeholder_label.deleteLater()
            self.placeholder_label = None
        
        # Add header
        header = QLabel(f"<h3>Specifications for {model}</h3>")
        header.setAlignment(Qt.AlignCenter)
        self.specs_layout.addWidget(header)
        
        # We'll use a common format for all products with the agreed order
        # Some sections might be product-specific
        self.add_voltage_section()
        self.add_material_section()
        self.add_probe_length_section()
        self.add_connection_section()
        self.add_exotic_metals_section()
        self.add_oring_section()
        self.add_cable_length_section()
        self.add_housing_section()
        self.add_additional_options_section()
            
        # Add spacer at the bottom
        self.specs_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        
        # Connect signals for all widgets
        for widget_name, widget in self.specs_widgets.items():
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.on_specs_changed)
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.valueChanged.connect(self.on_specs_changed)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.on_specs_changed)
            elif isinstance(widget, QSlider):
                widget.valueChanged.connect(self.on_specs_changed)
    
    def add_voltage_section(self):
        """Add voltage selection section."""
        group = QGroupBox("Voltage")
        layout = QFormLayout()
        
        voltage = QComboBox()
        voltage.addItems(["24 VDC", "120 VAC", "240 VAC"])
        layout.addRow("Supply Voltage:", voltage)
        self.specs_widgets["voltage"] = voltage
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_material_section(self):
        """Add material selection section."""
        group = QGroupBox("Material")
        layout = QFormLayout()
        
        material = QComboBox()
        material.addItems(["S - 316 Stainless Steel", "A - Aluminum", "H - Hastelloy C"])
        layout.addRow("Material:", material)
        self.specs_widgets["material"] = material
        
        # Add process material type if it's a level switch
        if "Level Switch" in self.current_product.get("category", ""):
            material_type = QComboBox()
            material_type.addItems(["Liquid", "Powder", "Granular", "Slurry"])
            layout.addRow("Process Material Type:", material_type)
            self.specs_widgets["material_type"] = material_type
            
            viscosity = QComboBox()
            viscosity.addItems(["Low", "Medium", "High", "Very High"])
            layout.addRow("Viscosity:", viscosity)
            self.specs_widgets["viscosity"] = viscosity
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_probe_length_section(self):
        """Add probe length section."""
        # Skip for products without probes
        if "Emissions" in self.current_product.get("category", ""):
            return
            
        group = QGroupBox("Probe Length")
        layout = QFormLayout()
        
        probe_length = QSpinBox()
        probe_length.setRange(1, 120)
        probe_length.setValue(12)
        probe_length.setSuffix(" inches")
        layout.addRow("Probe Length:", probe_length)
        self.specs_widgets["probe_length"] = probe_length
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_connection_section(self):
        """Add connection section."""
        group = QGroupBox("Connection")
        layout = QFormLayout()
        
        connection = QComboBox()
        connection.addItems(["1/2\" NPT", "3/4\" NPT", "1\" NPT", "1.5\" NPT", "2\" NPT", "Flanged"])
        layout.addRow("Process Connection:", connection)
        self.specs_widgets["connection"] = connection
        
        # Add mounting type for applicable products
        if "Level Switch" in self.current_product.get("category", ""):
            mounting = QComboBox()
            mounting.addItems(["Top Mount", "Side Mount", "Angled"])
            layout.addRow("Mounting Type:", mounting)
            self.specs_widgets["mounting"] = mounting
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_exotic_metals_section(self):
        """Add exotic metals section."""
        group = QGroupBox("Exotic Metals")
        layout = QFormLayout()
        
        exotic_metals = QComboBox()
        exotic_metals.addItems(["None", "T - Titanium", "U - Monel"])
        layout.addRow("Exotic Metal Option:", exotic_metals)
        self.specs_widgets["exotic_metals"] = exotic_metals
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_oring_section(self):
        """Add O-ring material section."""
        # Skip for products without O-rings
        if "Emissions" in self.current_product.get("category", ""):
            return
            
        group = QGroupBox("O-ring Material")
        layout = QFormLayout()
        
        oring = QComboBox()
        oring.addItems(["Viton", "PTFE", "Kalrez", "EPDM"])
        layout.addRow("O-ring Material:", oring)
        self.specs_widgets["oring"] = oring
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_cable_length_section(self):
        """Add cable length section."""
        group = QGroupBox("Cable Length")
        layout = QFormLayout()
        
        cable_length = QSpinBox()
        cable_length.setRange(0, 100)
        cable_length.setValue(10)
        cable_length.setSuffix(" feet")
        layout.addRow("Cable Length:", cable_length)
        self.specs_widgets["cable_length"] = cable_length
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_housing_section(self):
        """Add housing type section."""
        group = QGroupBox("Housing Type")
        layout = QFormLayout()
        
        housing = QComboBox()
        housing.addItems(["Standard", "Explosion-Proof", "Stainless Steel"])
        layout.addRow("Housing Type:", housing)
        self.specs_widgets["housing"] = housing
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_additional_options_section(self):
        """Add additional options section."""
        group = QGroupBox("Additional Options")
        layout = QVBoxLayout()
        
        # Common options for most products
        high_temp = QCheckBox("High Temperature Version")
        layout.addWidget(high_temp)
        self.specs_widgets["high_temp"] = high_temp
        
        # Product-specific options
        if "Level Switch" in self.current_product.get("category", ""):
            extended_probe = QCheckBox("Extended Probe")
            layout.addWidget(extended_probe)
            self.specs_widgets["extended_probe"] = extended_probe
        
        if "Transmitter" in self.current_product.get("category", ""):
            remote_display = QCheckBox("Remote Display Option")
            layout.addWidget(remote_display)
            self.specs_widgets["remote_display"] = remote_display
            
            output_type = QComboBox()
            output_type.addItems(["4-20mA", "0-10V", "Modbus RTU", "HART"])
            layout.addWidget(QLabel("Output Type:"))
            layout.addWidget(output_type)
            self.specs_widgets["output_type"] = output_type
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    # The following methods are kept for backward compatibility with 
    # existing code but are no longer used directly
    
    def add_point_level_specs(self):
        pass
        
    def add_continuous_measurement_specs(self):
        pass
    
    def add_multi_point_specs(self):
        pass
    
    def add_magnetic_level_specs(self):
        pass
    
    def add_dust_emissions_specs(self):
        pass
    
    def on_specs_changed(self):
        """Handle changes to specification values."""
        # Get all current specification values
        specs = self.get_specifications()
        
        # Emit signal with updated specifications
        self.specs_updated.emit(specs)
    
    def get_specifications(self):
        """Get all current specification values."""
        specs = {}
        
        # Extract values from all specification widgets
        for name, widget in self.specs_widgets.items():
            if isinstance(widget, QComboBox):
                specs[name] = widget.currentText()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                specs[name] = widget.value()
            elif isinstance(widget, QSlider):
                specs[name] = widget.value()
            elif isinstance(widget, QCheckBox):
                specs[name] = widget.isChecked()
            elif isinstance(widget, QLineEdit):
                specs[name] = widget.text()
        
        return specs 