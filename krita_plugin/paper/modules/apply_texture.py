from krita import *
import shutil
import os
import xml.etree.ElementTree as ET 
import hashlib
from PyQt5.QtGui import QImage
from .contrast import qimage_contrast_adjust
from.contrast_failsafe import contrast_failsafe

def make_texture(texture_path, pattern_name):
    path = Krita.instance().readSetting("", "ResourceDirectory", None)
    path = os.path.join(path, "patterns")
    file_path = path + "/" + pattern_name
    
    # Just overwrite, for now
    shutil.copyfile(texture_path, file_path)

    # Load copied file
    pattern_file_path = path + "/pattern_" + pattern_name
    shutil.copyfile(texture_path, pattern_file_path)
    img = QImage(pattern_file_path).convertToFormat(QImage.Format.Format_RGB888)
    if img:
        contrast_adjusted_img = contrast_failsafe(texture_path)
        contrast_adjusted_img.save(pattern_file_path)
    return pattern_file_path

def apply_texture(texture_path, pattern_name):
    # Ensure pattern exists
    path = make_texture(texture_path, pattern_name)
    PATTERN_NAME = "pattern_" + pattern_name
    # Krita.instance().resourcesChanged()
    
    # Apply paper file as pattern
    patterns_manager = Krita.instance().resources("pattern")
    pattern = None
    for name, res in patterns_manager.items():
        if name == PATTERN_NAME:
            pattern = res

    print(PATTERN_NAME)
    
    view = Krita.instance().activeWindow().activeView()
    if view and pattern:
        # Enable patterns
        preset = Preset(view.currentBrushPreset())
        root = ET.fromstring(preset.toXML())
        
        enabled = False
        named = False
        md5ed = False
        md5sumed = False
        for param in root.findall("param"):
            if param is not None and param.attrib["name"] == "Texture/Pattern/Enabled":
                enabled = True
                param.text = "true"
            if param is not None and param.attrib["name"] == "Texture/Pattern/PatternFileName":
                named = True
                param.text = PATTERN_NAME
            # if param is not None and param.attrib["name"] == "Texture/Pattern/PatternMD5":
            #     print(param.text)
            #     md5ed = True
            #     with open(texture_path, "rb") as f:
            #         param.text = hashlib.md5(f.read()).digest()
            if param is not None and param.attrib["name"] == "Texture/Pattern/PatternMD5Sum":
                md5sumed = True
                with open(path, "rb") as f:
                    param.text = hashlib.md5(f.read()).hexdigest()
                
        if not enabled:
            pattern_param = ET.Element("param", type="internal", name="Texture/Pattern/Enabled")
            pattern_param.text = "true"
            root.append(pattern_param)
        
        if not named:
            pattern_param = ET.Element("param", type="string", name="Texture/Pattern/PatternFileName")
            pattern_param.text = PATTERN_NAME
            root.append(pattern_param)
        
        # if not md5ed:
        #     pattern_param = ET.Element("param", type="string", name="Texture/Pattern/PatternMD5")
        #     with open(texture_path, "rb") as f:
        #         pattern_param.text = hashlib.md5(f.read()).digest()
        #     root.append(pattern_param)
        
        if not md5sumed:
            pattern_param = ET.Element("param", type="string", name="Texture/Pattern/PatternMD5Sum")
            with open(path, "rb") as f:
                pattern_param.text = hashlib.md5(f.read()).hexdigest()
            root.append(pattern_param)
        
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
        view.setCurrentBrushPreset(preset.fromXML(xml_string))
        
        # Set the current pattern
        view.activateResource(pattern)
        view.setCurrentPattern(pattern)
        
        doc = Krita.instance().activeDocument()
        doc.refreshProjection()
    else:
        print("Failed to find pattern!")