from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .texture import overlay_canvas
import os

class PaperDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper")

        self.mainWidget = QWidget(self)
        self.setWidget(self.mainWidget)

        self.papers = QListWidget()
        self.papers.setViewMode(QListWidget.IconMode)
        self.papers.setIconSize(QSize(64, 64))
        self.papers.setResizeMode(QListWidget.Adjust)

        layout = QVBoxLayout()
        layout.addWidget(self.papers)
        self.mainWidget.setLayout(layout)

        self.load_paper()

        self.papers.itemClicked.connect(self.click)

    def load_paper(self):
        """Loads paper from assets folder into docker."""
        assets = os.path.join(os.path.dirname(__file__), "../", "assets")

        for file in os.listdir(assets):
            path = os.path.join(assets, file)

            pixmap = QPixmap(path).scaled(64, 64)
            
            item = QListWidgetItem()
            item.setIcon(QIcon(pixmap))
            item.setData(32, path)  
            item.setToolTip(file) 

            self.papers.addItem(item)

    def click(self, item):
        """Calls texture functions when an item is clicked."""
        texture_path = item.data(32) 

        # Placeholder functions for Elaine and Ken to implement.
        self.apply_texture(texture_path)
        overlay_canvas("03_default-paper.png")

    def apply_texture(self, texture_path):
        """
        Placeholder function for applying texture as a heightmap or brush texture.
        """
        pass

    def canvasChanged(self, canvas):
        pass