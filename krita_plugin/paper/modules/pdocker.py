from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .texture import *
from .apply_texture import apply_texture
from .generate import generate_texture
import os

selection = [None, None]

class Paper(QWidget):
    def __init__(self):
        super().__init__()

        self.uniqueId = None

        self.paper = QListWidget()
        self.paper.setViewMode(QListWidget.IconMode)
        self.paper.setIconSize(QSize(64, 64))
        self.paper.setResizeMode(QListWidget.Adjust)
        self.paper.itemClicked.connect(self.paperclick)

        self.load()

        button = QPushButton("Apply")
        button.setToolTip("Applies the selected texture to your brush.")
        button.clicked.connect(self.buttonclick)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.paper)
        self.layout().addWidget(button)

    def load(self):
        self.paper.clear()
        assets = os.path.join(os.path.dirname(__file__), "../", "assets")

        for file in os.listdir(assets):
            path = os.path.join(assets, file)

            pixmap = QPixmap(path).scaled(64, 64)
            
            item = QListWidgetItem()
            item.setIcon(QIcon(pixmap))
            item.setData(32, path)
            item.setData(33, file)
            item.setToolTip(file)

            self.paper.addItem(item)

    def paperclick(self, item):
        path = item.data(32)
        file = item.data(33)

        self.uniqueId = overlay_canvas(file, self.uniqueId)
        selection[0], selection[1] = path, file

    def buttonclick(self):
        if not selection[0]:
            raise Exception("You need to select a paper!")
        
        apply_texture(selection[0], selection[1])

class PaperDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper")

        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
    
        self.paper = Paper()

        button = QPushButton("Generate New Paper")
        button.setToolTip("Generates the selected paper model in your current doc size.")
        button.clicked.connect(self.click)

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Model 1: Crumpled", "Model 2: Paper Foundation"])
        self.comboBox.setToolTip("Select a model.")

        layout = QHBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(button)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(self.paper)
        mainWidget.layout().addLayout(layout)

    def click(self):
        doc = Krita.instance().activeDocument()

        assets = os.path.join(os.path.dirname(__file__), "../assets")
        width, height, n = doc.width(), doc.height(), len(os.listdir(assets)) - 2

        if self.comboBox.currentText() == "Model 1: Crumpled":
            model_path = os.path.join(os.path.dirname(__file__), "models/crumpled-generator-006000_iterations.pth")
            file = f"crumpled_{width}x{height}_gen{n}.png"
        else:
            model_path = os.path.join(os.path.dirname(__file__), "models/paper_foundation-generator-010000_iterations.pth")
            file = f"paper_foundation_{width}x{height}_gen{n}.png"

        im = generate_texture(model_path, width, height)
        path = os.path.join(assets, file)
        im.save(path)

        self.paper.load()

        self.paper.uniqueId = overlay_canvas_file(path, self.paper.uniqueId)

    def canvasChanged(self, canvas):
        pass