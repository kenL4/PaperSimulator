from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .lighting import *
from .pdocker import selection
import math

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
        self.slider.setToolTip("Select the light intensity.")
        self.slider.valueChanged.connect(self.sync)

        self.spinBox = QDoubleSpinBox()
        self.spinBox.setRange(0, 100)
        self.spinBox.setSingleStep(0.1)
        self.spinBox.setSuffix("%")
        self.spinBox.setToolTip("Select the light intensity.")
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

class Incidence(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.draw(0)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 90)
        self.slider.setToolTip("Select the angle of incidence.")
        self.slider.valueChanged.connect(self.sync)

        self.spinBox = QDoubleSpinBox()
        self.spinBox.setRange(0, 90)
        self.spinBox.setSingleStep(0.1)
        self.spinBox.setSuffix("°")
        self.spinBox.setToolTip("Select the angle of incidence.")
        self.spinBox.valueChanged.connect(self.sync)

        layout = QHBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.spinBox)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout().addLayout(layout)

    def draw(self, value):
        pen = QPen(Qt.white, 1, Qt.DotLine)
        x, y = 35 + 30*math.cos(math.radians(value + 180)), 35 + 30*math.sin(math.radians(value + 180))

        pixmap = QPixmap(70, 40)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(Qt.transparent)
        painter.setBrush(QColor(56, 56, 56))
        painter.drawPie(QRect(5, 5, 60, 60), 0, 2880)
        
        painter.setPen(Qt.white)
        painter.drawLine(5, 35, 65, 35)
        painter.drawLine(QLineF(35, 35, x, y))

        painter.setBrush(Qt.white)  
        painter.drawEllipse(33, 33, 4, 4)
        painter.drawEllipse(QPointF(x, y), 2, 2)
        
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)  
        painter.drawArc(QRect(20, 20, 30, 30), 0, 2880)
        painter.drawLine(35, 5, 35, 35)

        painter.end()

        self.label.setPixmap(pixmap)

    def sync(self, value):
        self.slider.setValue(int(value))
        self.spinBox.setValue(value)

        self.draw(value)

class Direction(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.draw(0)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 360)
        self.slider.setToolTip("Select the light direction.")
        self.slider.valueChanged.connect(self.sync)

        self.spinBox = QDoubleSpinBox()
        self.spinBox.setRange(0, 360)
        self.spinBox.setSingleStep(0.1)
        self.spinBox.setSuffix("°")
        self.spinBox.setToolTip("Select the light direction.")
        self.spinBox.valueChanged.connect(self.sync)

        layout = QHBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.spinBox)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout().addLayout(layout)

    def draw(self, value):
        pixmap = QPixmap(70, 70)
        pixmap.fill(Qt.transparent)

        pen = QPen(Qt.white, 1, Qt.DotLine)
        x, y = 35 + 30*math.cos(math.radians(value)), 35 + 30*math.sin(math.radians(value))

        painter = QPainter(pixmap)
        
        painter.setPen(Qt.white)
        painter.setBrush(QColor(56, 56, 56)) 
        painter.drawEllipse(5, 5, 60, 60)
        painter.drawLine(QLineF(35, 35, x, y))
               
        painter.setBrush(Qt.white)
        painter.drawEllipse(33, 33, 4, 4)  
        painter.drawEllipse(QPointF(x, y), 2, 2)

        painter.setPen(pen)
        painter.setBrush(Qt.transparent)  
        painter.drawEllipse(20, 20, 30, 30)
        painter.drawLine(35, 5, 35, 65)
        painter.drawLine(5, 35, 65, 35)

        painter.end()

        self.label.setPixmap(pixmap)

    def sync(self, value):
        self.slider.setValue(int(value))
        self.spinBox.setValue(value)

        self.draw(value)

class LightDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Light")

        mainWidget = QWidget(self)
        self.setWidget(mainWidget)

        self.path = None
        
        self.intensity = Intensity()
        self.incidence = Incidence()
        self.direction = Direction()
        self.shading = Shading()

        button = QPushButton("Apply", mainWidget)
        button.setToolTip("Works best at low angles of incidence.")
        button.clicked.connect(self.click)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(self.intensity)
        mainWidget.layout().addWidget(self.incidence)
        mainWidget.layout().addWidget(self.direction)
        mainWidget.layout().addWidget(button)

    def click(self):
        if not selection[0]:
            raise Exception("You need to select a paper!")
        
        if self.path != selection[0]:
            self.path = selection[0]
            normal_map = generate_normal_map_from_image(self.path)
            self.shading.set_normal_map(normal_map)
        self.shading.update(self.incidence.slider.value(), self.direction.slider.value(), self.intensity.slider.value())

    def canvasChanged(self, canvas):
        pass