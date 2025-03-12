from krita import *
from PyQt5.QtWidgets import *
from .modules.apply_texture import make_texture
from .modules.pdocker import PaperDocker
from .modules.ldocker import LightDocker
import shutil
import os

assets_folder = os.path.join(os.path.dirname(__file__), "assets")
resource_path = Krita.instance().readSetting("", "ResourceDirectory", None)
pattern_path = os.path.join(resource_path, "patterns")
for root, dirs, files in os.walk(assets_folder):
    for file in files:
        shutil.copyfile(assets_folder + "/" + file, pattern_path + "/" + file)
        shutil.copyfile(assets_folder + "/" + file, pattern_path + "/pattern_" + file)
        make_texture(assets_folder + "/" + file, file)

Krita.instance().addDockWidgetFactory(DockWidgetFactory("pDocker", DockWidgetFactoryBase.DockRight, PaperDocker))
Krita.instance().addDockWidgetFactory(DockWidgetFactory("lDocker", DockWidgetFactoryBase.DockRight, LightDocker))