from krita import *
import struct
import math

def dot(u, v): #return the dot product of  two vectors
    if len(u) != len(v):
        raise Exception("vectors are the not the same dimensions")

    return sum(u[i] * v[i] for i in range(len(u)))

def get_shadow_node(normal_map, direction, doc): 
    #arguments: array of vectors, direction to the light source, document
    #all vector arguments should be normalised
    
    result = doc.createNode("shadow", "paintLayer")
    width = len(normal_map[0])
    height = len(normal_map)
    
    pixel_data = bytearray()
    for y in range(height):
        for x in range(width):
            intensity = dot(normal_map[y][x], direction)
            intensity = max(intensity, 0)
            gamma = 255 - int(255 * (intensity ** (1/2.2)))
            
            gamma = min(gamma, 255)
            gamma = max(gamma, 0)
            colour = (0, 0, 0, gamma)
            pixel_data.extend(struct.pack('BBBB', *colour))
            
    result.setPixelData(pixel_data, 0, 0, width, height)
    return result
    
    
def gen_funny_normal_map(width, height):
    result = [[(0, 0, 0) for y in range(width)] for x in range(height)]
    for j in range(height):
        for i in range(width):
            scale_factor = 1/50
            x = i * scale_factor
            y = j * scale_factor
            result[j][i] = (-math.cos(x) * scale_factor, math.sin(y) * scale_factor, 1)
            magnitude = result[j][i][0] * result[j][i][0]
            magnitude += result[j][i][1] * result[j][i][1]
            magnitude += result[j][i][2] * result[j][i][2]
            magnitude= math.sqrt(magnitude)
            if (magnitude == 0):
                continue
            result[j][i] = (result[j][i][0] / magnitude, result[j][i][1] / magnitude, result[j][i][2] / magnitude)
    return result
     
    

app = Krita.instance()

doc = app.activeDocument()

shadow_node = doc.createNode("shadow", "paintLayer")

width = doc.width()
height = doc.height()

normal_map = gen_funny_normal_map(width, height)

shadow_node = get_shadow_node(normal_map, (0.95 * 3.5, 0.2207 * 3.5, 0.2207 * 3.5), doc)

doc.rootNode().addChildNode(shadow_node, None)
doc.refreshProjection()