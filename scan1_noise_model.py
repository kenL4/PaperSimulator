import numpy as np
from PIL import Image
import math
import random

heightmap_im = Image.open("./scan1-heightmap.png")
heightmap_raw = np.array(heightmap_im)
heightmap = 1.0-(heightmap_raw/255.0)

def random_block_sample(heightmap, block_size, count):
    xs = np.random.randint(heightmap.shape[0] - block_size, size=count)
    ys = np.random.randint(heightmap.shape[1] - block_size, size=count)
    blocks = np.array([heightmap[x:x+block_size, y:y+block_size] for x in xs for y in ys])
    return blocks

def find_nearest_block(blocks, block):
    diff_block = blocks - block
    diff = np.sum(np.square(diff_block), axis=(1, 2))
    return blocks[np.argmin(diff)]

block_size = 8
paper_width = 50
paper_height = 50

block_influence = np.array([[
  max(0, 1.0 - math.pow(2*x/(block_size-1)-1.0, 2) - math.pow(2*y/(block_size-1)-1.0, 2))
  for x in range(block_size)] for y in range(block_size)
])
print("influence:\n", block_influence)

real_block = random_block_sample(heightmap, paper_width, 1)[0]
paper_noise = np.random.rand(paper_width, paper_height)*0.8

for i in range(1000):
    if i % 100 == 0:
        blocks = random_block_sample(heightmap, block_size, 200)
    if i % 200 == 0:
        print(i)
        draw = np.vstack((paper_noise, real_block))
        im = Image.fromarray(((1.0-draw)*255).astype(np.uint8))
        im.save(f"noise_{i:06d}.png")

    x = random.randint(0, paper_width-block_size)
    y = random.randint(0, paper_height-block_size)
    noise_block = paper_noise[x:x+block_size, y:y+block_size]
    nearest_block = find_nearest_block(blocks, noise_block)
    noise_block += block_influence * (nearest_block - noise_block)
