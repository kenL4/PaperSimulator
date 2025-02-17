from PIL import Image
import numpy as np
import itertools
import math


def create_perlin_lookup_table(cell_size):
    gradient_choices = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, -1]])
    gradient_indices = np.array(list(itertools.product(range(len(gradient_choices)), repeat=4)))
    print(gradient_indices)
    gradient_vectors = gradient_choices[gradient_indices]
    cell_axis = (np.arange(0, cell_size) + 0.5) / cell_size
    x, y = np.meshgrid(cell_axis, cell_axis)
    xy = np.stack((x, y), axis=2)
    distance_vectors = xy[:,:,np.newaxis,:] - [[0, 0], [1, 0], [0, 1], [1, 1]]
    influence_values = np.einsum('xycd,icd->ixyc', distance_vectors, gradient_vectors)
    def lerp(x1, x2, t):
        t = 6*np.power(t, 5) - 15*np.power(t, 4) + 10*np.power(t, 3)
        return x1 + t*(x2-x1)
    x1 = lerp(influence_values[:,:,:,0], influence_values[:,:,:,1], xy[:,:,0])
    x2 = lerp(influence_values[:,:,:,2], influence_values[:,:,:,3], xy[:,:,0])
    lookup_table = lerp(x1, x2, xy[:,:,1])
    return lookup_table

cell_size = 20
grid_width = 5
grid_height = 5

lookup_table = create_perlin_lookup_table(cell_size)

gradients = np.random.randint(8, size=(grid_width+1, grid_height+1))
cell_perlin_indices = 8*8*8*gradients[:-1,:-1] + 8*8*gradients[:-1,1:] + 8*gradients[1:,:-1] + gradients[1:,1:]

cell_contents = lookup_table[cell_perlin_indices]
heightmap = np.block([[cell_contents[i, j] for j in range(grid_height)] for i in range(grid_width)])

heightmap_norm = (heightmap - np.min(heightmap)) / (np.max(heightmap) - np.min(heightmap))
im = Image.fromarray((heightmap_norm*255).astype(np.uint8))
im.save("perlin_noise.png")

print("DONE")
