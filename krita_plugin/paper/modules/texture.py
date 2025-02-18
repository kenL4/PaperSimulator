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
    fill_layer.setLocked(True)

    w = InfoObject()
    w.setProperty("color", "white")
    fill_white = doc.createFillLayer("White Overlay", "color", w, s)

    root.addChildNode(fill_white, root.childNodes()[1])
    fill_white.setBlendingMode("overlay")
    fill_white.setVisible(True)
    fill_white.setLocked(True)

    doc.refreshProjection()