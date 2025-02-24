from krita import *
import shutil
import os
import xml.etree.ElementTree as ET 

def make_texture(texture_path, pattern_name):
    path = Krita.instance().readSetting("", "ResourceDirectory", None)
    path = os.path.join(path, "patterns")
    pattern_file_path = path + "/" + pattern_name
    
    # Just overwrite, for now
    shutil.copyfile(texture_path, pattern_file_path)
    print(pattern_file_path)
    return pattern_file_path

def apply_texture(texture_path, PATTERN_NAME):
    # Ensure pattern exists
    path = make_texture(texture_path, PATTERN_NAME)
    # Krita.instance().resourcesChanged()
    
    # Apply paper file as pattern
    patterns_manager = Krita.instance().resources("pattern")
    pattern = None
    for name, res in patterns_manager.items():
        if name == PATTERN_NAME:
            print("Pattern file found!")
            pattern = res
    
    view = Krita.instance().activeWindow().activeView()
    if view and pattern:
        # Enable patterns
        preset = Preset(view.currentBrushPreset())
        root = ET.fromstring(preset.toXML())
        
        written = False
        for param in root.findall("param"):
            if param is not None and param.attrib["name"] == "Texture/Pattern/Enabled":
                written = True
                param.text = "![CDATA[true]]"
                
        if not written:
            pattern_param = ET.Element("param", type="string", name="Texture/Pattern/Enabled")
            pattern_param.text = "![CDATA[true]]"
            root.append(pattern_param)
        
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
        # print(xml_string)
        view.setCurrentBrushPreset(preset.fromXML(xml_string))
        
        # Set the current pattern
        view.activateResource(pattern)
        view.setCurrentPattern(pattern)
        
        doc = Krita.instance().activeDocument()
        doc.refreshProjection()
    else:
        print("Failed to find pattern!")