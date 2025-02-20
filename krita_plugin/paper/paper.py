from krita import *
from PyQt5.QtWidgets import *
from .modules.pdocker import PaperDocker
from .modules.ldocker import LightDocker

Krita.instance().addDockWidgetFactory(DockWidgetFactory("pDocker", DockWidgetFactoryBase.DockRight, PaperDocker))
Krita.instance().addDockWidgetFactory(DockWidgetFactory("lDocker", DockWidgetFactoryBase.DockRight, LightDocker))