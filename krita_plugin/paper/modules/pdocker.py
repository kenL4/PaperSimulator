from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .texture import overlay_canvas
from .apply_texture import apply_texture
import os

class Paper():
    def __init__(self):
        super().__init__()

        self.uniqueId = None

        papers = QListWidget()
        papers.setViewMode(QListWidget.IconMode)
        papers.setIconSize(QSize(64, 64))
        papers.setResizeMode(QListWidget.Adjust)
        papers.itemClicked.connect(self.click)

        self.load(papers)

    def load(self, papers):
        assets = os.path.join(os.path.dirname(__file__), "../", "assets")

        for file in os.listdir(assets):
            path = os.path.join(assets, file)

            pixmap = QPixmap(path).scaled(64, 64)
            
            item = QListWidgetItem()
            item.setIcon(QIcon(pixmap))
            item.setData(32, path)
            item.setData(33, file)
            item.setToolTip(file)

            papers.addItem(item)

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
    
        papers = Paper()
        
        button = QPushButton("Generate New Paper", mainWidget)
        button.clicked.connect(self.click)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(papers)
        mainWidget.layout().addWidget(button)

    def click(self):
        doc = Krita.instance().activeDocument()
        
        # Placeholder function for Elaine to implement.

        #generate(doc.width(), doc.height())

    def canvasChanged(self, canvas):
        pass