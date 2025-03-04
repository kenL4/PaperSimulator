from krita import *

def overlay_canvas(texture_pattern, id):
    doc = Krita.instance().activeDocument()
    root = doc.rootNode()

    i = InfoObject()
    i.setProperty("pattern", texture_pattern)

    s = Selection()
    s.select(0, 0, doc.width(), doc.height(), 255)
    
    fill_layer = doc.createFillLayer(texture_pattern, "pattern", i, s)
    fill_layer.setLocked(True)
    
    # deal with duplication
    flag = False
    if id:
        for i, node in enumerate(root.childNodes()):
            if node.uniqueId() == id:
                root.addChildNode(fill_layer, root.childNodes()[i])
                node.remove()
                flag = True

    if not flag:
        root.addChildNode(fill_layer, root.childNodes()[0])

    doc.refreshProjection()
    return fill_layer.uniqueId()