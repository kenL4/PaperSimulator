import numpy as np
import pyvista as pv

def get_surface_normals(obj_file: str):
    mesh = pv.read(obj_file)
    mesh = mesh.compute_normals()

get_surface_normals("mesh_gen/test/sphere_mesh.obj")