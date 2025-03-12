#from krita import *
import math
import numpy as np
import time
from PIL import Image
import pyvista as pv
# sys.path.append("mesh_utils")
# import get_mesh_data
# import pointCloudGen

normal_constant_idk = 1

def heightmap_to_mesh(heightmap_np, true_width, true_height, true_depth):
    xs, ys = np.meshgrid(
      np.linspace(0, true_width, heightmap_np.shape[1]),
      np.linspace(0, true_height, heightmap_np.shape[0]),
    )
    grid = pv.StructuredGrid(xs, ys, heightmap_np * true_depth)
    mesh = grid.extract_surface()
    return mesh

def get_normal_map_from_heightmap(heightmap_np):
    height,width = heightmap_np.shape
    mesh = heightmap_to_mesh(heightmap_np, width, height, normal_constant_idk)
    mesh = mesh.compute_normals(cell_normals = False, point_normals = True)
    normals = mesh['Normals'].tolist()
    normalMap = np.array(normals)
    normalMap = np.reshape(normalMap, (height, width, 3))
    dir = np.take(normalMap, [2], axis=2)
    dir = dir / np.abs(dir)
    normalMap *= dir

    magnitude = np.linalg.norm(normalMap, axis=-1, keepdims=True)
    normalMap = normalMap / magnitude

    return normalMap

def generate_normal_map_from_image(image_path):
    dot = image_path.rfind(".")
    new_path = image_path[:dot] + "_normal.png"
    
    if (Path(new_path).is_file()):
        return get_normal_map_from_image(new_path)

    image = Image.open(image_path)
    #width, height = image.size

    result = np.array(image) / 255
    if (len(result.shape) == 3):
        result = np.mean(result, axis=2)

    result = get_normal_map_from_heightmap(result)
    normal_map_to_image(result, new_path)
    return get_normal_map_from_image(new_path)

def normal_map_to_image(normal_map, path):
    width, height, three = normal_map.shape
    result = np.copy(normal_map)
    result.resize(width, height, 3)
    result *= 32768
    result += np.ones(shape=(width, height, 3)) * 32768
    result = result.astype("int32")
    result1 = result // 256
    result1 = np.clip(result1, 0, 255)
    result2 = result % 256
    result = np.append(result1, result2, 0)
    result = result.astype("uint8")
    img = Image.fromarray(result, "RGB")
    img.save(path)

def get_normal_map_from_image(path):
    image = Image.open(path)
    width, height = image.size
    result = np.array(image).astype("float64")
    first = result[:height//2]
    second = result[height//2:]
    result = first * 256 + second
    height //= 2
    result.resize(width, height, 3)
    result -= np.ones(shape=(width, height, 3)) * 32768
    result = result / 32768

    result = np.swapaxes(result, 0, 1)

    width, height = height, width

    app = Krita.instance()
    doc = app.activeDocument()
    result = np.tile(result, (2,2))
    while width < doc.width() or height < doc.height():
        result = reflect_vector_pattern(result)
        width *= 2
        height *= 2

    return result

def reflect_vector_pattern(top_left):
    #takes numpy array and reflects it to create a pattern tile that is 4 times the size of the regular array
    top_right = np.fliplr(top_left) * np.array([1, -1, 1])
    bottom_left = np.flipud(top_left) * np.array([-1, 1, 1])
    bottom_right = np.fliplr(bottom_left) * np.array([1, -1, 1])

    top = np.append(top_left, top_right, 1)
    bottom = np.append(bottom_left, bottom_right, 1)
    new_arr = np.append(top, bottom, 0)

    return new_arr

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
        self.normal_map = np.array([])
        self.uniqueId = None

    def set_normal_map(self, normal_map):
        self.normal_map = normal_map

    def update_shadow_node(self, direction, shadow_node): 
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
        root = doc.rootNode()

        flag = False
        for i, node in enumerate(root.childNodes()):
            if node.uniqueId() == self.uniqueId:
                shadow_node = node
                flag = True

        if not flag:
            shadow_node = doc.createNode(SHADOW_LAYER_NAME, "paintLayer")
            shadow_node.setLocked(True)
            doc.rootNode().addChildNode(shadow_node, None)
            self.uniqueId = shadow_node.uniqueId()

        #width = doc.width()
        #height = doc.height()

        #normal_map = gen_funny_normal_map(width, height)

        start_time = time.time()
        self.update_shadow_node(direction, shadow_node)
        end_time = time.time()

        print(end_time - start_time)

        #doc.rootNode().addChildNode(shadow_node, None)
        doc.refreshProjection()

    def update(self, incidence_angle, angle, intensity):
        direction = np.array([0.0, 0.0, 0.0])
        angle_radians = angle / 180 * math.pi
        direction[0] = math.cos(angle_radians)
        direction[1] = math.sin(angle_radians)
        incidence_angle = incidence_angle / 180 * math.pi
        direction[2] = math.sin(incidence_angle)
        direction *= (intensity / 15)

        self.update_shading(direction)

if __name__ == "__main__":
    print(get_normal_map("catshockpaper.png"))
    app = Krita.instance()
    doc = app.activeDocument()
    shading = Shading()
    shading.set_normal_map(get_normal_map("catshockpaper.png"))
    shading.update_shading(np.array([1, 1, 0.7]))
