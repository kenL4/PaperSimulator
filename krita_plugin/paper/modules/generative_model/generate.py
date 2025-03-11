import torch
import numpy as np
from PIL import Image, ImageOps
import os
from pathlib import Path
import cv2


def generate_texture(model_fname, width, height):
    with torch.no_grad():
        device = torch.device('cpu')
        generator = torch.jit.load(model_fname, map_location=device)
        z = generator.random_latent_tensor(1, width, height)
        x = generator(z)[0, :, :height, :width]
        im_np = 255.0 * ((x[0, :, :].numpy() + 1.0) / 2.0)
        im = Image.fromarray(im_np.astype(np.uint8))
        return im


def generate():
    model_path = os.path.join(os.path.dirname(__file__), "models/paper_foundation-generator-010000_iterations.pth")
    im = generate_texture(model_path, 2000, 2000)
    return im


def make_pattern(arr):
    #takes numpy array and reflects it to create a pattern tile that is 4 times the size of the regular array

    top_left = make_pat_poissonblend3(arr)

    top_right = np.fliplr(top_left)
    bottom_left = np.flipud(top_left)
    bottom_right = np.fliplr(bottom_left)

    top = np.append(top_left, top_right, 1)
    bottom = np.append(bottom_left, bottom_right, 1)
    new_arr = np.append(top, bottom, 0)

    return new_arr



def make_pat_poissonblend2(src1):
    h, w = src1.shape
    edge = min(h,w)
    seam_size = edge // 2

    if seam_size % 2 != 0:
        seam_size -= 1

    edge = seam_size * 2

    src1 = src1[:edge,:edge]

    dst1 = np.roll(src1, seam_size, 1)
    mask1 = np.zeros_like(src1)
    mask1[:,-seam_size:] = 255

    src1 = cv2.cvtColor(src1, cv2.COLOR_GRAY2BGR)
    dst1 = cv2.cvtColor(dst1, cv2.COLOR_GRAY2BGR)

    centre1 = (edge - (seam_size // 2), edge // 2)

    output1 = cv2.seamlessClone(src1, dst1, mask1, centre1, cv2.NORMAL_CLONE)

    src2 = cv2.cvtColor(output1, cv2.COLOR_BGR2GRAY)
    dst2 = np.roll(src2, seam_size, 0)
    mask2 = np.zeros_like(src2)
    mask2[-seam_size:,:] = 255

    src2 = cv2.cvtColor(src2, cv2.COLOR_GRAY2BGR)
    dst2 = cv2.cvtColor(dst2, cv2.COLOR_GRAY2BGR)

    centre2 = (edge // 2, edge - (seam_size // 2))

    output2 = cv2.seamlessClone(src2, dst2, mask2, centre2, cv2.NORMAL_CLONE)
    return output2

def make_pat_poissonblend3(og_img_arr):
    h, w = og_img_arr.shape
    edge = min(h,w)
    seam_size = edge // 2

    if seam_size % 2 != 0:
        seam_size -= 1

    edge = seam_size * 2

    src1 = og_img_arr[:edge,:edge]

    dst1 = np.roll(src1, seam_size, 1)
    dst1 = np.roll(dst1, seam_size, 0)
    #mask1 = np.full(src1.shape, 255, dtype=np.uint8)
    mask1 = np.zeros(src1.shape, dtype=np.uint8)
    mask_seam = 10
    mask1[mask_seam:,:] = 255 #top
    mask1[:mask_seam,:] = 255 #bottom
    mask1[:,mask_seam:] = 255 #left
    mask1[:,:mask_seam] = 255 #right
    mask1[(seam_size - mask_seam):(seam_size + mask_seam), :] = 255
    mask1[:, (seam_size - mask_seam):(seam_size + mask_seam)] = 255
    mask = Image.fromarray(mask1)
    mask = mask.convert('RGB')
    mask.show()

    src1 = cv2.cvtColor(src1, cv2.COLOR_GRAY2BGR)
    dst1 = cv2.cvtColor(dst1, cv2.COLOR_GRAY2BGR)

    centre1 = (edge // 2, edge // 2)

    output1 = cv2.seamlessClone(src1, dst1, mask1, centre1, cv2.NORMAL_CLONE)
    return output1


def save_to_assets(im):
    save_path = Path(r"C:\Users\ejale\AppData\Roaming\krita\pykrita\paper\assets")
    im.save(os.path.join(save_path, "new_img.jpg"))
    print("saved successfully")
    return


if __name__ == "__main__":
    im = generate()
    im.show()
    im_arr = np.array(im)
    new_im_arr = make_pattern(im_arr)
    new_im = Image.fromarray(new_im_arr)
    new_im.show()
    #save_to_assets(new_im)