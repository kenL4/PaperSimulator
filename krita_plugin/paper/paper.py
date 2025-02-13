from krita import *
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
import os

class PaperPatternsDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper")

        # Create main widget (list of textures)
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
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # Only load image files
                texture_path = os.path.join(assets_folder, file_name)

                # Create list item with icon
                item = QListWidgetItem(file_name)
                pixmap = QPixmap(texture_path).scaled(64, 64)  # Resize for display
                item.setIcon(QIcon(pixmap))

                # Store full path in the item (for later retrieval)
                item.setData(32, texture_path)

                self.mainWidget.addItem(item)

    def handle_item_click(self, item):
        """Handles item clicks, calling functions to apply texture and overlay canvas."""
        texture_path = item.data(32)  # Get stored file path

        # Call the placeholder functions for Elaine and Ken to implement
        self.apply_texture(texture_path)
        self.overlay_canvas(texture_path)

    def apply_texture(self, texture_path):
        """
        Placeholder function for applying texture as a heightmap or brush texture.
        """
        pass

    def overlay_canvas(self, texture_path):
        """
        Placeholder function for applying the texture as an overlay on the canvas.
        """
        pass

    def canvasChanged(self, canvas):
        pass

class PaperPlugin(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        """Registers the Paper Textures Docker."""
        print("🔹 Setting up Paper Plugin...")
        factory = DockWidgetFactory("PaperTexturesDocker", DockWidgetFactoryBase.DockRight, PaperPatternsDocker)
        Krita.instance().addDockWidgetFactory(factory)

    def createActions(self, window):
        pass  # You can add menu actions here if needed


# Register the plugin
Krita.instance().addExtension(PaperPlugin(Krita.instance()))


