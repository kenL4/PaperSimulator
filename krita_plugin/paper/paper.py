from krita import *
from PyQt5.QtWidgets import *
from .modules.pdocker import PaperDocker

Krita.instance().addDockWidgetFactory(DockWidgetFactory("pDocker", DockWidgetFactoryBase.DockRight, PaperDocker))


