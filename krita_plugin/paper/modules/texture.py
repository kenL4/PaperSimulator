from krita import *

def overlay_canvas(texture_pattern):
    doc = Krita.instance().activeDocument()

    i = InfoObject()
    i.setProperty("pattern", texture_pattern)
    s = Selection()
    s.select(0, 0, doc.width(), doc.height(), 255)
    fill_layer = doc.createFillLayer("Paper Texture", "pattern", i, s)
    
    root = doc.rootNode()
    root.addChildNode(fill_layer, root.childNodes()[0])
    fill_layer.setVisible(True)
    fill_layer.setLocked(False)

    # + white overlay and merging
    i.setProperty("color", "white")
    white = doc.createFillLayer("", "color", i, s)

    root.addChildNode(white, root.childNodes()[1])
    white.setBlendingMode("overlay")
    white.setVisible(True)
    white.setLocked(False)

    white.mergeDown()
    background = doc.nodeByName("Background")
    background.setLocked(False)
    merged = doc.nodeByName("Paper Texture")
    merged.mergeDown()

    background.setLocked(True)

    doc.refreshProjection()