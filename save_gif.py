import os
from glob import glob
import imageio

src_folder = "/Users/jeff/OneDrive - City University of Hong Kong/study/Thesis/DefenseFigures/VarianceSnaps/SnapTextReverseAdded"
dst_file = "/Users/jeff/OneDrive - City University of Hong Kong/study/Thesis/DefenseFigures/VarianceSnaps/failed.gif"

img_files = sorted(glob(os.path.join(src_folder, "*01946.png")))
gif_images = []
for img_file in img_files:
    gif_images.append(imageio.imread(img_file))

imageio.mimsave(dst_file, gif_images, 'GIF', duration=0.5)