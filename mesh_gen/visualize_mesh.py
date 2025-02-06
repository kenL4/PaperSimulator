import numpy as np
import pyvista as pv

def visualize_mesh(obj_file: str):
    mesh = pv.read(obj_file)
    visual = mesh.plot()