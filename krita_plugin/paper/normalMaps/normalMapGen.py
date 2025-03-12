import math
import numpy as np
import time
from PIL import Image
import pyvista as pv


def generate_mesh(points_list, output_filename:str):
    points = pv.PolyData(points_list)
    surface_mesh = points.delaunay_2d()
    surface_mesh.save(output_filename)

def get_normal_map_from_heightmap(heightmap_np,height,width):


    generate_mesh(heightmap_np,"temp.obj")
    mesh = pv.read("temp.obj")
    mesh = mesh.compute_normals(cell_normals = False, point_normals = True)
    normals = mesh['Normals'].tolist()
    print(normals)
    normalMap = np.array(normals)
    normalMap = np.reshape(normalMap, (height, width, 3))
    dir = np.take(normalMap, [2], axis=2)
    dir = dir / np.abs(dir)
    normalMap *= dir

    magnitude = np.linalg.norm(normalMap, axis=-1, keepdims=True)
    normalMap = normalMap / magnitude

    return normalMap

def get_normal_map(image_path):
    image = Image.open(image_path).convert('L')

    result = np.array(image) / 255
    #ßresult.reshape(len(result)*len(result[0]),1)
    heightmap = []
    height,width = (len(result),len(result[0]))
    for x in range(len(result)):
        for y in range(len(result[0])):
            heightmap.append([x,y,result[x][y]])
    heightmap = np.array(heightmap)


    result = get_normal_map_from_heightmap(heightmap,height,width)
    return result

imagesToConvert = ["crumpled_3200x3200.png", "paper_foundation1_3200x3200.png", "paper_foundation2_1000x1000_gen1.png", "paper_foundating2_1920x1080.png"]


for fileName in imagesToConvert:
    print(fileName)
    normalMap = get_normal_map(fileName)
    if fileName == "test1.png":
        print(normalMap)
    file = open((fileName.split('.')[0]+".txt"),"w")    
    file.write(str(len(normalMap)) + '\n')
    file.write(str(len(normalMap[0])) + '\n')
    for line in normalMap:
        for term in line:
            file.write(str(term[0])+','+str(term[1])+','+str(term[2])+'\n')
    file.close()