from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from .texture import overlay_canvas
import os

class PaperDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper")

        # Create list of textures
        self.mainWidget = QListWidget()
        self.setWidget(self.mainWidget)

        # Load textures from assets folder
        self.load_textures()

        # Connect click event to apply texture
        self.mainWidget.itemClicked.connect(self.handle_item_click)

    def load_textures(self):
        """Loads texture images from the assets folder into the docker."""
        assets_folder = os.path.join(os.path.dirname(__file__), "assets")
        
        if not os.path.exists(assets_folder):
            print("Assets folder not found:", assets_folder)
            return
        
        for file_name in os.listdir(assets_folder):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                texture_path = os.path.join(assets_folder, file_name)

                # Create list item with icon
                item = QListWidgetItem(file_name)
                pixmap = QPixmap(texture_path).scaled(64, 64)  # Resize for display
                item.setIcon(QIcon(pixmap))

                # Store full path in the item 
                item.setData(32, texture_path)

                self.mainWidget.addItem(item)

    def handle_item_click(self, item):
        """Handles item clicks, calling functions to apply texture and overlay canvas."""
        texture_path = item.data(32)  # Get stored file path

        # Call the placeholder functions for Elaine and Ken to implement
        self.apply_texture(texture_path)
        overlay_canvas(self, "01_canvas.png")

    def apply_texture(self, texture_path):
        """
        Placeholder function for applying texture as a heightmap or brush texture.
        """
        pass

    def canvasChanged(self, canvas):
        pass