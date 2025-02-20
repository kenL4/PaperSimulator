from krita import *
import struct
import math
import numpy as np
import time

def dot(u, v): #return the dot product of  two vectors
    if len(u) != len(v):
        raise Exception("vectors are the not the same dimensions")

    return sum(u[i] * v[i] for i in range(len(u)))

def get_shadow_node(normal_map, direction, doc): 
    #arguments: array of vectors, direction to the light source, document
    #all vector arguments should be normalised
    #normal_map and direction should both be numpy arrays
    
    result = doc.createNode("shadow", "paintLayer")
    width = len(normal_map[0])
    height = len(normal_map)

    #get light intensity for each pixel
    dots = direction * normal_map
    dots = np.sum(dots, axis=2)
    dots[dots < 0] = 0

    #convert light intensity to alpha value in rbga
    gamma = np.ones([height, width], dtype=int) * 255 - ((dots ** (1/2.2)) * 255).astype(np.int32)
    gamma = np.clip(gamma, 0, 255)
    
    #convert to krita expected format
    colours = np.zeros([height, width, 3])
    gamma = np.expand_dims(gamma, axis=-1)
    colours = np.concatenate((colours, gamma), axis=-1)

    #convert to byte array
    colours = colours.astype(np.ubyte)
    pixel_data = colours.tobytes()
            
    result.setPixelData(pixel_data, 0, 0, width, height)
    return result
    
    
def gen_funny_normal_map(width, height):
    scale_factor = 1/50
    x = np.array([-math.cos(i * scale_factor) * scale_factor for i in range(width)])
    y = np.array([math.sin(i * scale_factor) * scale_factor for i in range(height)])

    x = np.expand_dims(x, axis=0)
    x = np.repeat(x, height, axis=0)
    #print(x.shape)
    y = np.expand_dims(y, axis=1)
    y = np.repeat(y, width, axis=1)
    z = np.ones([height, width, 1])

    x = np.expand_dims(x, axis=-1)
    y = np.expand_dims(y, axis=-1)

    result = np.concatenate((x, y, z), axis=-1)
    magnitude = np.linalg.norm(result, axis=-1, keepdims=True)
    result = result / magnitude
    return result

    

app = Krita.instance()

doc = app.activeDocument()

shadow_node = doc.createNode("shadow", "paintLayer")

width = doc.width()
height = doc.height()

normal_map = gen_funny_normal_map(width, height)

start_time = time.time()
shadow_node = get_shadow_node(normal_map, np.array([2, 1, 0.3]), doc)
end_time = time.time()

print(end_time - start_time)

doc.rootNode().addChildNode(shadow_node, None)
doc.refreshProjection()
