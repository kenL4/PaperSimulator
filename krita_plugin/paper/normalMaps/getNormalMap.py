import numpy as np

def getNormalMap(filename):
    file = open(filename)
    height = int(file.readline())
    width = int(file.readline())
    pointsText = file.readlines()
    points_list = []
    for line in pointsText:
        point = line.strip('\n').split(',')
        points_list.append([float(point[0]),float(point[1]),float(point[2])])
    points_np = np.array(points_list)
    points_final = np.reshape(points_np,(height,width,3))
    return points_final

