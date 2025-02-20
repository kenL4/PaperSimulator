from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from .lighting import *

class Angle(QWidget):
    def __init__(self):
        super().__init__()

        self.pixmap = QPixmap(100, 100)
        self.pixmap.fill(Qt.transparent)

        self.draw()

        self.label = QLabel()
        self.label.setPixmap(self.pixmap)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 360)
        self.slider.valueChanged.connect(self.sync)

        self.spinBox = QDoubleSpinBox()
        self.spinBox.setRange(0, 360)
        self.spinBox.setSingleStep(0.1)
        self.spinBox.setSuffix("°")
        self.spinBox.valueChanged.connect(self.sync)

        layout = QHBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.spinBox)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout().addLayout(layout)

    def draw(self):
        painter = QPainter(self.pixmap)        
        painter.setPen(Qt.black)
        painter.drawEllipse(10, 10, 80, 80)
        painter.drawLine(50, 50, 90, 50)
        painter.end()

    def sync(self, value):
        self.slider.setValue(int(value))
        self.spinBox.setValue(value)

        self.pixmap = self.pixmap.transformed(QTransform().rotate(-value))
        self.label.setPixmap(self.pixmap)

class Intensity(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.label.setFixedHeight(10)
        self.label.setStyleSheet("background-color: black; border-radius: 5px;")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.sync)

        self.spinBox = QDoubleSpinBox()
        self.spinBox.setRange(0, 100)
        self.spinBox.setSingleStep(0.1)
        self.spinBox.setSuffix("%")
        self.spinBox.valueChanged.connect(self.sync)

        layout = QHBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.spinBox)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addLayout(layout)

    def sync(self, value):
        self.slider.setValue(int(value))
        self.spinBox.setValue(value)

        brightness = int((value / 100) * 255)
        color = f"rgb({brightness}, {brightness}, {brightness})"
        self.label.setStyleSheet(f"background-color: {color}; border-radius: 5px;")

class LightDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Light")

        mainWidget = QWidget(self)
        self.setWidget(mainWidget)

        self.angle = Angle()
        self.intensity = Intensity()

        button = QPushButton("Apply", mainWidget)
        button.clicked.connect(self.click)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(self.angle)
        mainWidget.layout().addWidget(self.intensity)
        mainWidget.layout().addWidget(button)

    def click(self):
        # Placeholder function for Will and Jonathan.
        pass

    def canvasChanged(self, canvas):
        pass