from PIL import Image
import numpy as np

width = 500
height = 500
scale = 100
grid_width = (width-1)//scale + 2
grid_height = (height-1)//scale + 2
x_axis = (np.arange(0, width) + 0.5) / scale
y_axis = (np.arange(0, height) + 0.5) / scale
x, y = np.meshgrid(x_axis, y_axis)
xy = np.stack((x, y), axis=2)
cell = np.trunc(xy).astype(np.int32)
cell_corners = cell[:,:,np.newaxis,:] + [[0, 0], [1, 0], [0, 1], [1, 1]]
distance_vectors = xy[:,:,np.newaxis,:] - cell_corners
gradient_vectors = np.random.rand(grid_width, grid_height, 2)-0.5
gradient_vectors = gradient_vectors / np.linalg.norm(gradient_vectors, axis=2)[:,:,np.newaxis]
corner_gradients = gradient_vectors[cell_corners[:,:,:,0], cell_corners[:,:,:,1]]
dot_corners = np.einsum('xycd,xycd->xyc', distance_vectors, corner_gradients)
unit_xy = xy - cell
corner_weights = unit_xy
def lerp(x1, x2, t):
    t = 6*np.power(t, 5) - 15*np.power(t, 4) + 10*np.power(t, 3)
    return x1 + t*(x2-x1)
x1 = lerp(dot_corners[:,:,0], dot_corners[:,:,1], unit_xy[:,:,0])
x2 = lerp(dot_corners[:,:,2], dot_corners[:,:,3], unit_xy[:,:,0])
noise_np = lerp(x1, x2, unit_xy[:,:,1])

noise_np = (noise_np - np.min(noise_np)) / (np.max(noise_np) - np.min(noise_np))
noise_im = Image.fromarray((noise_np*255).astype(np.uint8))
noise_im.save("perlin_noise.png")
