import os
from tqdm import tqdm
from glob import glob


# read and set mtl files
file_names = glob("/Users/jeff/OneDrive - City University of Hong Kong/paper/7_AtlasCell/Code/Evaluation/Results/3DErrorVolumeTif/*.mtl")
for file_name in tqdm(file_names):
    with open(file_name, "r") as f:
        lines = f.readlines()

    out_lines = []
    for line in lines:
        if line.startswith("d "):
            line = line.replace("0.3", "0.1")
        out_lines.append(line)

    # and write everything back
    with open(file_name, 'w') as file:
        file.writelines(out_lines)
