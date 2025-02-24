from krita import *
import shutil
import os

def make_texture(texture_path, pattern_name):
    path = Krita.instance().readSetting("", "ResourceDirectory", None)
    path = os.path.join(path, "patterns")
    pattern_file_path = path + "/" + pattern_name
    
    # Just overwrite, for now
    try:
        shutil.copyfile(texture_path, pattern_file_path)
    except:
        print("Could not write to path!")
    print(pattern_file_path)
    return pattern_file_path

def apply_texture(texture_path, PATTERN_NAME):
    # Ensure pattern exists
    path = make_texture(texture_path, PATTERN_NAME)
    
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
        # preset = Preset(view.currentBrushPreset())
        # print(preset)
        
        # Set the current pattern
        view.setCurrentPattern(pattern)
        view.activateResource("pattern")
        
        doc = Krita.instance().activeDocument()
        doc.refreshProjection()
    else:
        print("Failed to apply pattern!")