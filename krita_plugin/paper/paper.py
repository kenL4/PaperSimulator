# THIS IS WHAT KRITA CALLS

from PyQt5.QtWidgets import *
from krita import *

class MyDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paper")

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("myDocker", DockWidgetFactoryBase.DockRight, MyDocker))# THIS IS WHAT KRITA CALLS