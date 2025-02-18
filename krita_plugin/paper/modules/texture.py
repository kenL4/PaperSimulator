from krita import *

def overlay_canvas(self, texture_pattern):
    doc = Krita.instance().activeDocument()

    i = InfoObject()
    i.setProperty("pattern", texture_pattern)
    s = Selection()
    s.select(0,0,doc.width(),doc.height(),255)
    fill_layer = doc.createFillLayer("Paper Texture", "pattern", i, s)
    
    root = doc.rootNode()
    root.addChildNode(fill_layer, root.childNodes()[0])
    fill_layer.setVisible(True)
    fill_layer.setLocked(True)

    doc.refreshProjection()