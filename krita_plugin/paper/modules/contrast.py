import numpy as np
from PyQt5.QtGui import QImage
import os

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
    normalized_img = (img - min_brightness) / (contrast) * 255
    return np.clip(normalized_img, 0, 255).astype(np.uint8)

def qimage_contrast_adjust(qimg):
    np_img = qimage_to_np(qimg)
    contrast_enhanced = contrast_stretch(np_img)
    return np_to_qimage(contrast_enhanced)

def test_contrast():
    # Avoid importing unnecessarily
    from PIL import Image

    path = os.path.join(os.getcwd(), 'test_assets/test_woods.jpg')
    img = Image.open(path)
    img.show()
    contrast_np = contrast_stretch(np.asarray(img))
    contrast_img = Image.fromarray(contrast_np)
    contrast_img.show()