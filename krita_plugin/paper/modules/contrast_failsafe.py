from PyQt5.QtGui import *
from .lighting import generate_normal_map_from_image
import numpy as np
import math

def contrast_failsafe(path):
    normal_map = generate_normal_map_from_image(path)
    
    # copy-paste of Will/Johnathan's code with hard-coded raking lighting
    direction = np.array([0.0, 0.0, 0.0])
    angle_radians = 90 / 180 * math.pi
    direction[0] = math.cos(angle_radians)
    direction[1] = math.sin(angle_radians)
    incidence_angle = 1 / 180 * math.pi
    direction[2] = math.sin(incidence_angle)
    direction *= (20 / 15)
        
    width = len(normal_map[0])
    height = len(normal_map)

    dots = direction * normal_map
    dots = np.sum(dots, axis=2)
    dots[dots < 0] = 0

    gamma = np.ones([height, width], dtype=int) * 255 - ((dots ** (1/2.2)) * 255).astype(np.int32)
    gamma = np.clip(gamma, 0, 255)

    colours = np.zeros([height, width, 4], dtype=np.uint8) 
    colours[..., 3] = gamma  

    return QImage(colours.data, width, height, QImage.Format_RGBA8888)