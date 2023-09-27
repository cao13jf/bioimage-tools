import os
import shutil
import numpy as np
import nibabel as nib

import os
import shutil
from PIL import Image
import numpy as np
import math

def scale2index(seg0):
    """Rescale all labels into range [0, 255]"""
    seg = seg0 % 255
    reduce_mask = np.logical_and(seg0!=0, seg==0)
    seg[reduce_mask] = 255  # Because only 255 colors are available, all cells should be numbered within [0, 255].
    seg = seg.astype(np.uint8)

    return seg

def check_folder(file_folder, overwrite=False):
    if "." in file_folder:
        file_folder = os.path.dirname(file_folder)
    if os.path.isdir(file_folder) and overwrite:
        shutil.rmtree(file_folder)
    elif not os.path.isdir(file_folder):
        os.makedirs(file_folder)


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


def get_cell_surface_mask(cell_volume):
    """
    Extract cell surface SegMemb from the volume segmentation
    :param cell_volume: cell volume SegMemb with the membrane embedded
    :return cell_surface: cell surface with only surface pixels
    """
    cell_mask = cell_volume == 0
    strel = morphology.ball(2)
    dilated_cell_mask = ndimage.binary_dilation(cell_mask, strel, iterations=1)
    surface_mask = np.logical_and(~cell_mask, dilated_cell_mask)
    surface_seg = cell_volume
    surface_seg[~surface_mask] = 0

    return surface_seg

