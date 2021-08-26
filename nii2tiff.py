import os
from glob import glob
import pandas as pd
import math
import shutil
from tqdm import tqdm
import numpy as np
from PIL import Image
from skimage.transform import resize

from utils.utils import nib_load, scale2index, save_indexed_tif, nib_save

#  =====================
#  save cells at particular frames
#  =====================
cell_name = "ABar"
src_folder = "/Users/jeff/OneDrive - City University of Hong Kong/paper/6_NCommunication/Submission/CShaper Supplementary Data/Segmentation Results/SegmentedCell/Sample04LabelUnified"
dst_folder = "/Users/jeff/OneDrive - City University of Hong Kong/study/Thesis/DefenseFigures/VarianceSnaps/Example"

# read name dictionary

seg_files = sorted(glob(os.path.join(src_folder, "*_error.nii.gz")))

# new labels file
label_file = os.path.join(os.path.dirname(dst_folder), os.path.basename(dst_folder) + ".txt")
# open(label_file, "w").close()

for tp in tqdm(range(len(seg_files)), desc=f"Saving to {dst_folder}"):
    seg_file = seg_files[tp]
    seg = nib_load(seg_file)

    seg = scale2index(seg)
    save_file = os.path.join(dst_folder, os.path.basename(seg_file).split(".")[0] + ".tif")
    save_indexed_tif(seg, save_file)

    # save label anchor
    label_anchor = np.unique(seg).tolist()[-1]
    with open(label_file, "a") as f:
        f.write(f"{label_anchor}\n")

