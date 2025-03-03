import torch
import numpy as np
from sgan_models import SGAN4_Generator
import PIL.Image

latent_width = 4
latent_height = 4
count = 10
generator_weights_fname = "generator_weights.pth"

generator = SGAN4_Generator()
generator.load_state_dict(
    torch.load(
        generator_weights_fname,
        weights_only=True,
        map_location=torch.device('cpu'),
    )
)

with torch.no_grad():
    for i in range(count):
        z = generator.random_latent_tensor(1, latent_width, latent_height)
        x = generator(z)
        x_img = 255.0 * ((x[0, 0, :, :].numpy() + 1.0) / 2.0)
        im = PIL.Image.fromarray(x_img.astype(np.uint8))
        im.save(f"output_{i+1:02d}.png")
