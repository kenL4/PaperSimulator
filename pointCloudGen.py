import numpy as np
from PIL import Image
import pyvista as pv


def infer_heightmap(img_fname, scale):
    # I couldnt figure out exactly what encoding scheme was used to map height
    # to color but its *roughly* HSV where H maps to height. This is good enough for
    # a prototype.
    im_rgb_orig = Image.open(img_fname)
    im_rgb = im_rgb_orig.resize((int(im_rgb_orig.width*scale), int(im_rgb_orig.height*scale)))
    im_hsv = im_rgb.convert("HSV")
    np_hsv = np.array(im_hsv)
    np_grey = np_hsv[:,:,0]
    np_grey_normalised = (np_grey - np.min(np_grey)) / (np.max(np_grey) - np.min(np_grey))
    return 1.0-np_grey_normalised

# Convert (unscaled) heightmap to (scaled) pointcloud. We know the
# width,height,depth by looking at the scale bars in the miscroscope images.
def heightmap_to_pointcloud(heightmap_np, true_width, true_height, true_depth):
    xs, ys = np.meshgrid(
      np.linspace(0, true_width, heightmap_np.shape[1]),
      np.linspace(0, true_height, heightmap_np.shape[0]),
    )
    pointcloud = np.stack(
      [ xs.ravel(), ys.ravel(), heightmap_np.ravel() * true_depth ],
      axis=1
    )
    return pointcloud


def heightmap_to_mesh(heightmap_np, true_width, true_height, true_depth):
    xs, ys = np.meshgrid(
      np.linspace(0, true_width, heightmap_np.shape[1]),
      np.linspace(0, true_height, heightmap_np.shape[0]),
    )
    grid = pv.StructuredGrid(xs, ys, heightmap_np * true_depth)
    mesh = grid.extract_surface()
    return mesh


def get_mesh_from_scan(scanFile,true_width, true_height, true_depth):
    heightmap = infer_heightmap(scanFile, 1.0)
    mesh = heightmap_to_mesh(heightmap,true_width, true_height, true_depth)
    return mesh