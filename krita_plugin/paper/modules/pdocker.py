from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .texture import overlay_canvas
import os

class PaperDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper")

        mainWidget = QWidget(self)
        self.setWidget(mainWidget)

        papers = QListWidget()
        papers.setViewMode(QListWidget.IconMode)
        papers.setIconSize(QSize(64, 64))
        papers.setResizeMode(QListWidget.Adjust)
        papers.itemClicked.connect(self.click)

        self.load(papers)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(papers)

    def load(self, papers):
        assets = os.path.join(os.path.dirname(__file__), "../", "assets")

        for file in os.listdir(assets):
            path = os.path.join(assets, file)

            pixmap = QPixmap(path).scaled(64, 64)
            
            item = QListWidgetItem()
            item.setIcon(QIcon(pixmap))
            item.setData(32, path)
            item.setToolTip(file)

            papers.addItem(item)

    def click(self, item):
        texture = item.data(32) 

        # Placeholder functions for Elaine and Ken to implement.
        #apply_texture(texture)
        overlay_canvas("03_default-paper.png")

    def canvasChanged(self, canvas):
        pass