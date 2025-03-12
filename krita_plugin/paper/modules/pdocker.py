from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .texture import *
from .apply_texture import apply_texture
from .generate import generate_texture
import os

selection = [None]

stylesheet = """QPushButton {
                        background-color: #fff;      
                        color: #000;                    
                        border: 1px solid #000;     
                        font-size: 14px;              
                        border-radius: 4px; 
                        padding: 2px;           
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;    
                        border: 2px solid #444;     
                    }
                    QPushButton:pressed {
                        background-color: #ddd;       
                        border: 2px solid #222;       
                        color: #222;                  
                    }
                    QPushButton:disabled {
                        background-color: #bbb;     
                        color: #666;                  
                        border: 2px solid #888;        
                    }"""

class Paper(QWidget):
    def __init__(self):
        super().__init__()

        self.uniqueId = None
        self.item = None

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
            item.setData(34, True)
            item.setToolTip(file)

            self.paper.addItem(item)

    def click(self, item):
        path = item.data(32)
        file = item.data(33)
        flag = item.data(34)

        if not flag:
            raise Exception("Restart to use!")

        self.uniqueId = overlay_canvas(file, self.uniqueId)
        selection[0] = path
        self.item = item

class PaperDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper")

        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
    
        self.paper = Paper()

        generate = QPushButton("Generate")
        generate.setToolTip("Generates the selected paper model in your current doc size.")
        generate.clicked.connect(self.generateclick)

        apply = QPushButton("Apply")
        apply.setStyleSheet(stylesheet)
        apply.setToolTip("Applies the selected texture to your brush.")
        apply.clicked.connect(self.applyclick)

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Model 1: Crumpled", "Model 2: Paper Foundation 1", "Model 3: Paper Foundation 2"])
        self.comboBox.setToolTip("Select a model.")

        layout = QHBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(generate)

        mainWidget.setLayout(QVBoxLayout())
        mainWidget.layout().addWidget(self.paper)
        mainWidget.layout().addLayout(layout)
        mainWidget.layout().addWidget(apply)

    def generateclick(self):
        doc = Krita.instance().activeDocument()

        assets = os.path.join(os.path.dirname(__file__), "../assets")
        width, height, n = doc.width(), doc.height(), len(os.listdir(assets)) - 3

        if self.comboBox.currentText() == "Model 1: Crumpled":
            model_path = os.path.join(os.path.dirname(__file__), "models/crumpled-generator-006000_iterations.pth")
            file = f"crumpled_{width}x{height}_gen{n}.png"
        elif self.comboBox.currentText() == "Model 2: Paper Foundation 1":
            model_path = os.path.join(os.path.dirname(__file__), "models/paper_foundation-generator-010000_iterations.pth")
            file = f"paper_foundation1_{width}x{height}_gen{n}.png"
        else:
            model_path = os.path.join(os.path.dirname(__file__), "models/paper_foundation_online-generator-006000_iterations.pth")
            file = f"paper_foundation2_{width}x{height}_gen{n}.png"

        im = generate_texture(model_path, width, height)
        path = os.path.join(assets, file)
        im.save(path)

        pixmap = QPixmap(path).scaled(64, 64)

        item = QListWidgetItem()
        item.setIcon(QIcon(pixmap))
        item.setData(32, path)
        item.setData(33, file)
        item.setData(34, False)
        item.setToolTip("Restart to use!")

        self.paper.paper.addItem(item)

        self.paper.uniqueId = overlay_canvas_file(path, file, self.paper.uniqueId)

    def applyclick(self):
        if not selection[0]:
            raise Exception("You need to select a paper!")
        
        item = self.paper.item
        
        path = item.data(32)
        file = item.data(33)
        flag = item.data(34)

        if not flag:
            raise Exception("Restart to use!")
        
        apply_texture(path, file)

    def canvasChanged(self, canvas):
        pass