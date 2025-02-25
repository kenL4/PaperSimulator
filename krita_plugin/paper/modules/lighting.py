from krita import *
import struct
import math
import numpy as np
import time
import pyvista as pv
import sys
sys.path.append("mesh_utils")
import get_mesh_data
import pointCloudGen


def get_normal_map_from_heightmap(heightmap_np):
    (height,width) = heightmap_np.shape()
    mesh = pointCloudGen.heightmap_to_mesh()
    mesh = mesh.compute_normals(cell_normals = False, point_normals = True)
    normals = mesh['Normals'].tolist()
    normalMap = [normals[width*i:width*(i+1)] for i in range(height)]
    return (height,width,normalMap)


    

def get_normal_map_from_obj_file(objFile,origHeight,origWidth):
    #For prototype1 height and width is 1623x1125
    meshNormals = get_mesh_data.get_mesh_with_surface_normals(objFile)
    normals = meshNormals['Normals'].tolist()

    #Map to 3D array
    normalMap = [normals[origWidth*i:origWidth*(i+1)] for i in range(origHeight)]

    return (origHeight,origWidth,normalMap)

SHADOW_LAYER_NAME = "shadow"


def reflect_pattern(top_left):
    #takes numpy array and reflects it to create a pattern tile that is 4 times the size of the regular array
    top_right = np.fliplr(top_left)
    bottom_left = np.flipud(top_left)
    bottom_right = np.fliplr(bottom_left)

    top = np.append(top_left, top_right, 1)
    bottom = np.append(bottom_left, bottom_right, 1)
    new_arr = np.append(top, bottom, 0)

    return new_arr


def dot(u, v): #return the dot product of  two vectors
    if len(u) != len(v):
        raise Exception("vectors are the not the same dimensions")

    return sum(u[i] * v[i] for i in range(len(u)))

def gen_funny_normal_map(width, height): #for testing only
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

class Shading:
    def __init__(self):
        self.normal_map = None

    def set_normal_map(self, normal_map):
        self.normal_map = normal_map

    def update_shadow_node(self, direction, doc, shadow_node): 
        #arguments: array of vectors, direction to the light source, document
        #all vector arguments should be normalised
        #normal_map and direction should both be numpy arrays
        
        width = len(self.normal_map[0])
        height = len(self.normal_map)

        #get light intensity for each pixel
        dots = direction * self.normal_map
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
                
        shadow_node.setPixelData(pixel_data, 0, 0, width, height)
        return shadow_node
    
    def update_shading(self, direction):
        if (self.normal_map.shape[0] == 0):
            raise Exception("normal map is not set")
        
        app = Krita.instance()
        doc = app.activeDocument()

        shadow_node = doc.nodeByName(SHADOW_LAYER_NAME)
        if shadow_node == None:
            shadow_node = doc.createNode(SHADOW_LAYER_NAME, "paintLayer")
            doc.rootNode().addChildNode(shadow_node, None)

        width = doc.width()
        height = doc.height()

        #normal_map = gen_funny_normal_map(width, height)

        start_time = time.time()
        self.update_shadow_node(direction, doc, shadow_node)
        end_time = time.time()

        print(end_time - start_time)

        #doc.rootNode().addChildNode(shadow_node, None)
        doc.refreshProjection()

if __name__ == "__main__":
    app = Krita.instance()
    doc = app.activeDocument()
    shading = Shading()
    shading.set_normal_map(gen_funny_normal_map(doc.width(), doc.height()))
    shading.update_shading(np.array([1, 1, 0.7]))
