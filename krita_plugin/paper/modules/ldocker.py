from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from .lighting import *

class AngleSelector(QWidget):
    def __init__(self):
        super().__init__()

        # Create Layout
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()

        # Custom Circular Display (Rotating Image)
        self.image_label = QLabel()
        self.base_pixmap = QPixmap(100, 100)
        self.base_pixmap.fill(Qt.transparent)
        self.draw_circle_with_arrow(self.base_pixmap)
        self.image_label.setPixmap(self.base_pixmap)

        # Angle Slider (Horizontal for Logical Control)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 360)
        self.slider.setValue(0)

        # Angle Display (Numeric Input)
        self.spinBox = QDoubleSpinBox()
        self.spinBox.setRange(0, 360)
        self.spinBox.setSingleStep(0.1)
        self.spinBox.setSuffix("°")

        # Sync Slider and SpinBox
        self.slider.valueChanged.connect(self.sync_spinbox)
        self.spinBox.valueChanged.connect(self.sync_slider)

        # Add Widgets to Layout
        control_layout.addWidget(self.slider)
        control_layout.addWidget(self.spinBox)

        main_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(control_layout)
        self.setLayout(main_layout)

    def sync_spinbox(self, value):
        self.spinBox.setValue(value)
        self.update_angle_display(value)

    def sync_slider(self, value):
        self.slider.setValue(int(value))
        self.update_angle_display(value)

    def update_angle_display(self, angle):
        """ Rotates the arrow to match the selected angle. """
        rotated_pixmap = self.base_pixmap.transformed(QTransform().rotate(-angle))
        self.image_label.setPixmap(rotated_pixmap)

    def draw_circle_with_arrow(self, pixmap):
        """ Draws a simple compass-like indicator with an arrow pointing to 0° (right). """
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw outer circle
        painter.setPen(Qt.black)
        painter.drawEllipse(10, 10, 80, 80)

        # Draw center arrow (pointing right initially, 0° direction)
        painter.drawLine(50, 50, 90, 50)
        painter.end()

class LightIntensitySlider(QWidget):
    def __init__(self):
        super().__init__()

        # Main Layout
        main_layout = QVBoxLayout()

        # Brightness Display (Thinner)
        self.light_label = QLabel()
        self.light_label.setFixedHeight(30)  # Thinner appearance
        self.light_label.setStyleSheet("background-color: black; border-radius: 5px;")

        # Horizontal Layout for Slider & SpinBox
        control_layout = QHBoxLayout()

        # Slider for Light Intensity (0% to 100%)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)  # Start at 0%
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)

        # SpinBox for Numeric Input
        self.spinBox = QDoubleSpinBox()
        self.spinBox.setRange(0, 100)
        self.spinBox.setSingleStep(1.0)  # Step size
        self.spinBox.setSuffix("%")  # Show percentage symbol
        self.spinBox.setValue(0)  # Start at 0%
        self.spinBox.setFixedWidth(60)  # Keep it compact

        # Sync Slider and SpinBox
        self.slider.valueChanged.connect(self.sync_spinbox)
        self.spinBox.valueChanged.connect(self.sync_slider)

        # Add Slider & SpinBox to Horizontal Layout
        control_layout.addWidget(self.slider)
        control_layout.addWidget(self.spinBox)

        # Add Widgets to Main Layout
        main_layout.addWidget(self.light_label)
        main_layout.addLayout(control_layout)
        self.setLayout(main_layout)

    def sync_spinbox(self, value):
        """ Sync SpinBox when Slider changes. """
        self.spinBox.setValue(value)
        self.update_light_intensity(value)

    def sync_slider(self, value):
        """ Sync Slider when SpinBox changes. """
        self.slider.setValue(int(value))
        self.update_light_intensity(value)

    def update_light_intensity(self, value):
        """ Update label background based on intensity level. """
        brightness = int((value / 100) * 255)  # Convert 0-100% to 0-255 color range
        color = f"rgb({brightness}, {brightness}, {brightness})"
        self.light_label.setStyleSheet(f"background-color: {color}; border-radius: 5px;")

class LightDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Light")

        mainWidget = QWidget(self)
        self.setWidget(mainWidget)

        self.angle = AngleSelector()
        self.intensity = LightIntensitySlider()
        button = QPushButton("Apply", mainWidget)
        button.clicked.connect(self.light)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(self.angle)
        mainWidget.layout().addWidget(self.intensity)
        mainWidget.layout().addWidget(button)

    def light(self):
        # Placeholder function for Will and Jonathan.
        angle = self.angle.slider.value()
        intensity = self.intensity.slider.value()
        pass

    def canvasChanged(self, canvas):
        pass