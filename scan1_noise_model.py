import numpy as np
from PIL import Image
import math
import random
import scipy


def random_block_sample(heightmap, block_size, count):
    xs = np.random.randint(heightmap.shape[0] - block_size, size=count)
    ys = np.random.randint(heightmap.shape[1] - block_size, size=count)
    blocks = np.array([heightmap[x:x+block_size, y:y+block_size] for x in xs for y in ys])
    return blocks

def find_nearest_block(blocks, block):
    diff_block = blocks - block
    diff = np.sum(np.square(diff_block), axis=(1, 2))
    return blocks[np.argmin(diff)]

def converge_heightmaps(
        sample_heightmap,
        heightmap,
        block_size,
        iterations,
        resample_frequency=100,
        resample_size=8):
    assert heightmap.ndim == 2
    assert sample_heightmap.ndim == 2
    assert heightmap.shape[0] >= block_size
    assert heightmap.shape[1] >= block_size
    assert sample_heightmap.ndim == 2
    assert sample_heightmap.shape[0] >= block_size
    assert sample_heightmap.shape[1] >= block_size

    block_influence = np.array([[
      max(0, 1.0 - math.pow(2*x/(block_size-1)-1.0, 2) - math.pow(2*y/(block_size-1)-1.0, 2))
      for x in range(block_size)] for y in range(block_size)
    ])

    sample_blocks = None
    for i in range(iterations):
        if i % resample_frequency == 0:
            sample_blocks = random_block_sample(sample_heightmap, block_size, resample_size)
        x = random.randint(0, heightmap.shape[0]-block_size)
        y = random.randint(0, heightmap.shape[1]-block_size)
        block = heightmap[x:x+block_size, y:y+block_size]
        nearest_block = find_nearest_block(sample_blocks, block)
        block += block_influence * (nearest_block - block)



sample_im = Image.open("./scan1-heightmap.png")
sample_raw = np.array(sample_im)
sample = 1.0-(sample_raw/255.0)

paper_width = 1623
paper_height = 925

steps = [
# scale, block_size, noise, iterations-per-unit-area, resample_frequency, resample_size
  (20,  8, 1.00, 0.003,  10, 20),
  (20,  8, 0.40, 0.001,  10, 20),
  (20,  8, 0.20, 0.001,  10, 20),
  (10,  8, 0.05, 0.005,  50, 20),
  (10,  8, 0.01, 0.003,  50, 20),
  ( 5, 10, 0.05, 0.005,  50, 20),
  ( 3,  8, 0.02, 0.005,  50, 40),
  ( 1,  6, 0.00, 0.050, 500, 20)
]

heightmap = np.zeros((paper_height, paper_width))

print("start")
for i,(scale, block_size, noise, ipa, resample_frequency, resample_size) in enumerate(steps):
    iterations = int(ipa * heightmap.size)
    heightmap_scaled = scipy.ndimage.zoom(heightmap, 1/scale)
    heightmap_scaled \
        = (1.0-noise) * heightmap_scaled \
        +       noise * np.random.rand(*heightmap_scaled.shape)
    sample_scaled = scipy.ndimage.zoom(sample, 1/scale)
    converge_heightmaps(sample_scaled, heightmap_scaled, block_size, iterations, resample_frequency, resample_size)
    heightmap = scipy.ndimage.zoom(heightmap_scaled, scale)

    print(f"{i}")
    im = Image.fromarray(((1.0-heightmap)*255).astype(np.uint8))
    im.save(f"noise_{i:06d}.png")
