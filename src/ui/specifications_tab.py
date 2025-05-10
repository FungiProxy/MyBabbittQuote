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
        
        # Create different specs based on category
        if "Point Level" in category:
            self.add_point_level_specs()
        elif "Continuous Measurement" in category:
            self.add_continuous_measurement_specs()
        elif "Multi-Point" in category:
            self.add_multi_point_specs()
        elif "Magnetic Level" in category:
            self.add_magnetic_level_specs()
        else:  # Dust Emissions
            self.add_dust_emissions_specs()
            
        # Add spacer at the bottom
        self.specs_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
    
    def add_point_level_specs(self):
        """Add specifications for Point Level Switches."""
        # Material type
        material_group = QGroupBox("Material Properties")
        material_layout = QFormLayout()
        
        material_type = QComboBox()
        material_type.addItems(["Liquid", "Powder", "Granular", "Slurry"])
        material_layout.addRow("Material Type:", material_type)
        self.specs_widgets["material_type"] = material_type
        
        # Viscosity (for liquids)
        viscosity = QComboBox()
        viscosity.addItems(["Low", "Medium", "High", "Very High"])
        material_layout.addRow("Viscosity:", viscosity)
        self.specs_widgets["viscosity"] = viscosity
        
        # Temperature range
        temp_min = QSpinBox()
        temp_min.setRange(-100, 500)
        temp_min.setValue(20)
        temp_min.setSuffix(" °C")
        material_layout.addRow("Minimum Temperature:", temp_min)
        self.specs_widgets["temp_min"] = temp_min
        
        temp_max = QSpinBox()
        temp_max.setRange(-100, 500)
        temp_max.setValue(80)
        temp_max.setSuffix(" °C")
        material_layout.addRow("Maximum Temperature:", temp_max)
        self.specs_widgets["temp_max"] = temp_max
        
        material_group.setLayout(material_layout)
        self.specs_layout.addWidget(material_group)
        
        # Installation options
        install_group = QGroupBox("Installation Options")
        install_layout = QFormLayout()
        
        mounting = QComboBox()
        mounting.addItems(["Top Mount", "Side Mount", "Angled"])
        install_layout.addRow("Mounting Type:", mounting)
        self.specs_widgets["mounting"] = mounting
        
        connection = QComboBox()
        connection.addItems(["1/2\" NPT", "3/4\" NPT", "1\" NPT", "1.5\" NPT", "2\" NPT", "Flanged"])
        install_layout.addRow("Process Connection:", connection)
        self.specs_widgets["connection"] = connection
        
        probe_length = QSpinBox()
        probe_length.setRange(1, 120)
        probe_length.setValue(12)
        probe_length.setSuffix(" inches")
        install_layout.addRow("Probe Length:", probe_length)
        self.specs_widgets["probe_length"] = probe_length
        
        install_group.setLayout(install_layout)
        self.specs_layout.addWidget(install_group)
        
        # Electrical options
        electrical_group = QGroupBox("Electrical Options")
        electrical_layout = QFormLayout()
        
        voltage = QComboBox()
        voltage.addItems(["24 VDC", "120 VAC", "240 VAC"])
        electrical_layout.addRow("Supply Voltage:", voltage)
        self.specs_widgets["voltage"] = voltage
        
        output = QComboBox()
        output.addItems(["Relay SPDT", "Relay DPDT", "4-20mA", "0-10V", "Modbus RTU"])
        electrical_layout.addRow("Output Type:", output)
        self.specs_widgets["output"] = output
        
        electrical_group.setLayout(electrical_layout)
        self.specs_layout.addWidget(electrical_group)
        
        # Additional options
        options_group = QGroupBox("Additional Options")
        options_layout = QVBoxLayout()
        
        explosion_proof = QCheckBox("Explosion Proof Enclosure")
        options_layout.addWidget(explosion_proof)
        self.specs_widgets["explosion_proof"] = explosion_proof
        
        high_temp = QCheckBox("High Temperature Version")
        options_layout.addWidget(high_temp)
        self.specs_widgets["high_temp"] = high_temp
        
        extended_probe = QCheckBox("Extended Probe")
        options_layout.addWidget(extended_probe)
        self.specs_widgets["extended_probe"] = extended_probe
        
        options_group.setLayout(options_layout)
        self.specs_layout.addWidget(options_group)
        
        # Connect signals
        for widget_name, widget in self.specs_widgets.items():
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.on_specs_changed)
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.valueChanged.connect(self.on_specs_changed)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.on_specs_changed)
    
    def add_continuous_measurement_specs(self):
        """Add specifications for Continuous Measurement Transmitters."""
        # Basic placeholder - would be filled with relevant controls
        range_group = QGroupBox("Measurement Range")
        range_layout = QFormLayout()
        
        min_range = QDoubleSpinBox()
        min_range.setRange(0, 1000)
        min_range.setValue(0)
        min_range.setSuffix(" ft")
        range_layout.addRow("Minimum Range:", min_range)
        self.specs_widgets["min_range"] = min_range
        
        max_range = QDoubleSpinBox()
        max_range.setRange(0, 1000)
        max_range.setValue(30)
        max_range.setSuffix(" ft")
        range_layout.addRow("Maximum Range:", max_range)
        self.specs_widgets["max_range"] = max_range
        
        range_group.setLayout(range_layout)
        self.specs_layout.addWidget(range_group)
        
        # Add more relevant controls for continuous measurement
        # ...
    
    def add_multi_point_specs(self):
        """Add specifications for Multi-Point Level Switches."""
        # Basic placeholder - would be filled with relevant controls
        points_group = QGroupBox("Switch Points")
        points_layout = QFormLayout()
        
        num_points = QSpinBox()
        num_points.setRange(1, 8)
        num_points.setValue(3)
        points_layout.addRow("Number of Switch Points:", num_points)
        self.specs_widgets["num_points"] = num_points
        
        points_group.setLayout(points_layout)
        self.specs_layout.addWidget(points_group)
        
        # Add more relevant controls for multi-point switches
        # ...
    
    def add_magnetic_level_specs(self):
        """Add specifications for Magnetic Level Indicators."""
        # Basic placeholder - would be filled with relevant controls
        indicator_group = QGroupBox("Indicator Options")
        indicator_layout = QFormLayout()
        
        indicator_length = QSpinBox()
        indicator_length.setRange(1, 200)
        indicator_length.setValue(36)
        indicator_length.setSuffix(" inches")
        indicator_layout.addRow("Indicator Length:", indicator_length)
        self.specs_widgets["indicator_length"] = indicator_length
        
        indicator_group.setLayout(indicator_layout)
        self.specs_layout.addWidget(indicator_group)
        
        # Add more relevant controls for magnetic level indicators
        # ...
    
    def add_dust_emissions_specs(self):
        """Add specifications for Dust Emissions Monitors."""
        # Basic placeholder - would be filled with relevant controls
        sensitivity_group = QGroupBox("Sensitivity")
        sensitivity_layout = QFormLayout()
        
        sensitivity = QSlider(Qt.Horizontal)
        sensitivity.setRange(1, 10)
        sensitivity.setValue(5)
        
        sensitivity_label = QLabel("5")
        sensitivity.valueChanged.connect(lambda v: sensitivity_label.setText(str(v)))
        
        sensitivity_layout.addRow("Sensitivity Level:", sensitivity)
        sensitivity_layout.addRow("Value:", sensitivity_label)
        self.specs_widgets["sensitivity"] = sensitivity
        
        sensitivity_group.setLayout(sensitivity_layout)
        self.specs_layout.addWidget(sensitivity_group)
        
        # Add more relevant controls for dust emissions monitors
        # ...
    
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