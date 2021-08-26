import os
import shutil
import numpy as np
import nibabel as nib

import os
import shutil
from PIL import Image
import numpy as np
import math


P = [252, 233, 79, 114, 159, 207, 239, 41, 41, 173, 127, 168, 138, 226, 52,
     233, 185, 110, 252, 175, 62, 211, 215, 207, 196, 160, 0, 32, 74, 135, 164, 0, 0,
     92, 53, 102, 78, 154, 6, 143, 89, 2, 206, 92, 0, 136, 138, 133, 237, 212, 0, 52,
     101, 164, 204, 0, 0, 117, 80, 123, 115, 210, 22, 193, 125, 17, 245, 121, 0, 186,
     189, 182, 85, 87, 83, 46, 52, 54, 238, 238, 236, 0, 0, 10, 252, 233, 89, 114, 159,
     217, 239, 41, 51, 173, 127, 178, 138, 226, 62, 233, 185, 120, 252, 175, 72, 211, 215,
     217, 196, 160, 10, 32, 74, 145, 164, 0, 10, 92, 53, 112, 78, 154, 16, 143, 89, 12,
     206, 92, 10, 136, 138, 143, 237, 212, 10, 52, 101, 174, 204, 0, 10, 117, 80, 133, 115,
     210, 32, 193, 125, 27, 245, 121, 10, 186, 189, 192, 85, 87, 93, 46, 52, 64, 238, 238, 246]

P = P * math.floor(255*3/len(P))
l = int(255 - len(P)/3)
P = P + P[3:(l+1)*3]
P = [0,0,0] + P

def read_tif(fname):
    img = Image.open(fname)
    h, w = np.shape(img)
    tiffarray = np.zeros((h, w, img.n_frames))
    for i in range(img.n_frames):
        img.seek(i)
        tiffarray[:, :, i] = np.array(img)

    return tiffarray

def read_indexed_png(fname):
    im = Image.open(fname)
    palette = im.getpalette()
    im = np.array(im)
    return im, palette

def scale2index(seg0):
    """Rescale all labels into range [0, 255]"""
    seg = seg0 % 255
    reduce_mask = np.logical_and(seg0!=0, seg==0)
    seg[reduce_mask] = 255  # Because only 255 colors are available, all cells should be numbered within [0, 255].
    seg = seg.astype(np.uint8)

    return seg

def save_indexed_png(fname, label_map, palette=P):
    if label_map.max() > 255:
        label_map = np.remainder(label_map, 255)
    label_map = np.squeeze(label_map.astype(np.uint8))
    im = Image.fromarray(label_map, 'P')
    im.putpalette(palette)
    im.save(fname, 'PNG')

def save_indexed_tif(fname, label_map, palette=P):
    raw_map = label_map.copy()
    if label_map.max() > 255:
        label_map = np.remainder(label_map, 255)
    label_map = np.squeeze(label_map.astype(np.uint8))
    label_map[np.logical_and(raw_map, ~label_map)] = 255
    im = Image.fromarray(label_map, 'P')
    im.putpalette(palette)
    im.save(fname)


def check_folder(file_folder, overwrite=False):
    if "." in file_folder:
        file_folder = os.path.dirname(file_folder)
    if os.path.isdir(file_folder) and overwrite:
        shutil.rmtree(file_folder)
    elif not os.path.isdir(file_folder):
        os.makedirs(file_folder)

def nib_save(file_name, data, overwrite=False):
    check_folder(file_name, overwrite)
    img = nib.Nifti1Image(data, np.eye(4))
    nib.save(img, file_name)

def nib_load(file_name):
    assert os.path.isfile(file_name), "File {} not exist".format(file_name)

    return nib.load(file_name).get_fdata()


def save_indexed_tif(file_name, data):
    """Save matrix data as indexed images which can be rendered by ImageJ"""
    check_folder(file_name)

    tif_imgs = []
    num_slices = data.shape[-1]
    for i_slice in range(num_slices):
        tif_img = Image.fromarray(data[..., i_slice], mode="P")
        tif_img.putpalette(P)
        tif_imgs.append(tif_img)
    if os.path.isfile(file_name):
        os.remove(file_name)

    # save the 1th slice image, treat others slices as appending
    tif_imgs[0].save(file_name, save_all=True, append_images=tif_imgs[1:])


def get_boundary(seg, b_width=1):
    """
    Get boundary of instance segmentation as white front pixels
    """
    padded = np.pad(seg, b_width, mode='edge')

    ndim = seg.ndim
    if ndim == 2:
        border_pixels = np.logical_and(
            np.logical_and(seg == padded[:-(2*b_width), b_width:-b_width], seg == padded[(2*b_width):, b_width:-b_width]),
            np.logical_and(seg == padded[b_width:-b_width, :-2*b_width], seg == padded[b_width:-b_width, 2*b_width:])
        )
    elif ndim == 3:
        border_pixels = np.logical_and(
            np.logical_and(seg == padded[:-(2 * b_width), b_width:-b_width, b_width:-b_width],
                           seg == padded[(2 * b_width):, b_width:-b_width, b_width:-b_width]),
            np.logical_and(seg == padded[b_width:-b_width, :-2 * b_width, b_width:-b_width],
                           seg == padded[b_width:-b_width, 2 * b_width:, b_width:-b_width])
        )
        border_pixels = np.logical_and(
            border_pixels,
            np.logical_and(seg == padded[b_width:-b_width, b_width:-b_width, :-2 * b_width],
                           seg == padded[b_width:-b_width, b_width:-b_width, 2 * b_width:])
        )

    # border_pixels = np.logical_not(border_pixels).astype(np.uint8)
    border_pixels = (border_pixels == 0).astype(np.uint8)

    return border_pixels * 255
