from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .texture import overlay_canvas
from .apply_texture import apply_texture
import os

class Paper(QWidget):
    def __init__(self):
        super().__init__()

        self.uniqueId = None

        self.paper = QListWidget()
        self.paper.setViewMode(QListWidget.IconMode)
        self.paper.setIconSize(QSize(64, 64))
        self.paper.setResizeMode(QListWidget.Adjust)
        self.paper.itemClicked.connect(self.click)

        self.load()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.paper)

    def load(self):
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

    def click(self, item):
        path = item.data(32)
        file = item.data(33)

        # Placeholder functions for Elaine and Ken to implement.
        self.uniqueId = overlay_canvas(file, self.uniqueId)
        apply_texture(path, file)

class PaperDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper")

        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
    
        paper = Paper()
        
        button = QPushButton("Generate New Paper", mainWidget)
        button.setToolTip("Generates the same paper model selected in your current doc size.")
        button.clicked.connect(self.click)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(paper)
        mainWidget.layout().addWidget(button)

    def click(self):
        doc = Krita.instance().activeDocument()
        
        # Placeholder function for Elaine to implement.

        #generate(doc.width(), doc.height())

    def canvasChanged(self, canvas):
        pass