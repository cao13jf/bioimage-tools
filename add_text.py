import os
from tqdm import tqdm
from PIL import ImageDraw, ImageFont, Image
from glob import glob

cell_name = "ABaraapppp"
root_folder = r"/Users/jeff/OneDrive - City University of Hong Kong/study/Thesis/DefenseFigures/VarianceSnaps/failedMesh"

file_list = glob(os.path.join(root_folder, "*.png"))
file_list.sort()

save_folder = os.path.join(os.path.dirname(root_folder), "SnapTextReverseAdded")
if not os.path.isdir(save_folder):
    os.makedirs(save_folder)


font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 52)
for i, file in enumerate(tqdm(file_list, desc="Renaming"), start=120):
    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    draw.text((600, 960), "Time: {:>8.2f} min".format((i + 1) * 1.43), (0, 0, 0), font=font)
    draw.text((600, 1000), f"Cell name: {cell_name}", (0, 0, 0), font=font)
    img.save(os.path.join(save_folder, os.path.basename(file)))
