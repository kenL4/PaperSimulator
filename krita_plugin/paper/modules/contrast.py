import numpy as np
from PIL import Image
import os

def contrast_stretch(img):
    min_brightness = np.min(img, axis=(0, 1), keepdims=True)
    max_brightness = np.max(img, axis=(0, 1), keepdims=True)
    contrast = max_brightness - min_brightness
    normalized_img = (img - min_brightness) / (contrast) * 255
    return np.clip(normalized_img, 0, 255).astype(np.uint8)

def test_contrast():
    path = os.path.join(os.getcwd(), 'test_assets/test_woods.jpg')
    img = Image.open(path)
    img.show()
    contrast_np = contrast_stretch(np.asarray(img))
    contrast_img = Image.fromarray(contrast_np)
    contrast_img.show()