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
# cell_name = "ABar"
# name_dict_file = "/Users/jeff/OneDrive - City University of Hong Kong/paper/6_NCommunication/Submission/CShaper Supplementary Data/Segmentation Results/name_dictionary.csv"
# src_folder = "/Users/jeff/OneDrive - City University of Hong Kong/paper/6_NCommunication/Submission/CShaper Supplementary Data/Segmentation Results/SegmentedCell/Sample04LabelUnified"
# dst_folder = "/Users/jeff/OneDrive - City University of Hong Kong/study/Thesis/DefenseFigures/VarianceSnaps/Example"
# start_frame = 5  # TODO: add automatic frames
# end_frame = 10
#
# # read name dictionary
# pd_number = pd.read_csv(name_dict_file, names=["name", "label"])
# number_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()
# name2label_dict= dict((v, k) for k, v in number_dict.items())
# label2name_dict = dict((k, v) for k, v in number_dict.items())
#
# cell_label = int(name2label_dict[cell_name])
# seg_files = sorted(glob(os.path.join(src_folder, "*.nii.gz")))
#
# # new labels file
# label_file = os.path.join(os.path.dirname(dst_folder), os.path.basename(dst_folder) + ".txt")
# # open(label_file, "w").close()
#
# for tp in tqdm(range(start_frame-1, end_frame, 1), desc=f"Saving to {dst_folder}"):
#     seg_file = seg_files[tp]
#     seg = nib_load(seg_file)
#     seg[seg != cell_label] = 0
#
#     seg = scale2index(seg)
#     save_file = os.path.join(dst_folder, os.path.basename(seg_file).split(".")[0] + "_" + cell_name + ".tif")
#     save_indexed_tif(seg, save_file)
#
#     # save label anchor
#     label_anchor = np.unique(seg).tolist()[-1]
#     with open(label_file, "a") as f:
#         f.write(f"{label_anchor}\n")


# =======================
# Save nii as tif
# =======================
nii_file = "/Users/jeff/OneDrive - City University of Hong Kong/study/Thesis/DefenseFigures/ActiveContour/Sample02_054_rawMemb.nii.gz"
save_file = nii_file.replace(".nii.gz", ".tif")
out_size = [205, 285, 134]
seg = nib_load(nii_file)
seg = np.flip(seg, axis=-1)
# seg = resize(image=seg, output_shape=out_size, preserve_range=True, order=0).astype(np.uint8)



