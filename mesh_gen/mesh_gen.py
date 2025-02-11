import numpy as np
import pyvista as pv
import pandas as pd
import os

def generate_mesh(points_filename: str, output_filename:str, delimiter: str):
    points_list = np.genfromtxt(points_filename, delimiter=delimiter, dtype=np.float32)
    points = pv.PolyData(points_list)
    surface_mesh = points.reconstruct_surface()
    surface_mesh.save(output_filename)

def test_sphere_mesh():
    from visualize_mesh import visualize_mesh
    def save_test_sphere_mesh(output_filename: str):
        N = 1000
        r = 1
        phis = np.random.uniform(0, 2 * np.pi, N)
        thetas = np.arccos(2 * np.random.uniform(0, 1, N) - 1)

        (xs, ys, zs) = r * (np.sin(thetas) * np.cos(phis), np.sin(thetas) * np.sin(phis), np.cos(thetas))

        df = pd.DataFrame({'x':xs, 'y':ys, 'z':zs})
        df.to_csv(output_filename, index=False)
        return df
    sphere_points_file = os.path.join(os.path.dirname(__file__), "test/sphere_points.csv")
    save_test_sphere_mesh(sphere_points_file)
    sphere_mesh_file = os.path.join(os.path.dirname(__file__), "test/sphere_mesh.obj")
    generate_mesh(sphere_points_file, sphere_mesh_file, delimiter=",")
    visualize_mesh(sphere_mesh_file)