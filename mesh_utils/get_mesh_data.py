import numpy as np
import pyvista as pv

def get_mesh_with_surface_normals(obj_file: str):
    mesh = pv.read(obj_file)
    mesh = mesh.compute_normals()
    return mesh