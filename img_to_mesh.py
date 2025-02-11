from pointCloudGen import get_point_cloud
from mesh_gen.mesh_gen import generate_mesh
from mesh_gen.visualize_mesh import visualize_mesh

img_file = "paper_img.webp"
points_filename = "paper_point_cloud.csv"
mesh_filename = "paper_mesh.obj"

get_point_cloud(img_file, points_filename)
generate_mesh(points_filename, mesh_filename, delimiter=",")
visualize_mesh(mesh_filename)