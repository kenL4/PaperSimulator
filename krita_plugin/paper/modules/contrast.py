import numpy as np
from PyQt5.QtGui import QImage
import os
import cv2

def qimage_to_np(img):
    img = img.convertToFormat(QImage.Format.Format_RGB888)
    w, h = img.width(), img.height()

    img_bits = img.bits()
    img_bits.setsize(w * h * 3)
    np_img = np.frombuffer(img_bits, dtype=np.uint8).reshape((h, w, 3))

    return np_img

def np_to_qimage(img):
    h, w, _ = img.shape
    byte_alignment = 3 * w
    return QImage(img.data, w, h, byte_alignment, QImage.Format.Format_RGB888).copy()

def contrast_stretch(img):
    min_brightness = np.min(img, axis=(0, 1), keepdims=True)
    max_brightness = np.max(img, axis=(0, 1), keepdims=True)
    contrast = max_brightness - min_brightness
    contrast = np.where(contrast == 0, 1, contrast)

    normalized_img = (img - min_brightness) / (contrast) * 255
    new_img = np.clip(normalized_img, 0, 255).astype(np.uint8)

    sobelx = cv2.Sobel(new_img, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(new_img, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.hypot(sobelx, sobely)
    sobel = sobel / sobel.max() * 255 # Normalize the edges
    sobel = sobel.astype(np.uint8)

    darkened = cv2.subtract(new_img, sobel)
    darkened = new_img
    return darkened

def quantize_img(img, colour_bits=1):
    # Make it black or white
    img = (img * (2**(colour_bits))) // (2**(colour_bits))
    return img

def qimage_contrast_adjust(qimg):
    np_img = qimage_to_np(qimg)
    gray_np = np.dot(np_img[..., :3], [0.2989, 0.5870, 0.1140])
    gray_rgb_np = np.stack([gray_np]*3, axis=-1).astype(np.uint8)
    contrast_enhanced = contrast_stretch(gray_rgb_np)
    mean = np.mean(contrast_enhanced, axis=(0,1))
    contrast_enhanced = np.where(contrast_enhanced < mean, 0, contrast_enhanced) # Hard boundary make look good
    return np_to_qimage(contrast_enhanced)

def test_contrast():
    # Avoid importing unnecessarily
    from PIL import Image

    path = os.path.join(os.getcwd(), 'krita_plugin/paper/assets/test1.png')
    img = Image.open(path).convert("RGB")
    gray_np = np.dot(np.asarray(img)[..., :3], [0.2989, 0.5870, 0.1140])
    gray_rgb_np = np.stack([gray_np]*3, axis=-1).astype(np.uint8)
    Image.fromarray(gray_rgb_np).show()
    contrast_np = contrast_stretch(gray_rgb_np)
    mean = np.mean(contrast_np, axis=(0,1))
    contrast_np = np.where(contrast_np < mean, 0, contrast_np)
    contrast_img = Image.fromarray(contrast_np)
    contrast_img.show()

if __name__ == "__main__":
    test_contrast()