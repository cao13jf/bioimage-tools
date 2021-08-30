import bpy
import os
import sys
import glob
from math import radians

## command run

# argv = sys.argv
# argv = argv[argv.index("--") + 1:] 
# input_folder = argv[0] # input folder
# save_folder = argv[1] # output folder
# obj_files = glob.glob(os.path.join(input_folder, "*.obj"))

# command run
# input_folder = "./VarianceSnaps/ExampleMesh"
# save_folder = "./ExampleMesh"
# obj_files = glob.glob(os.path.join(input_folder, "*.obj"))
# obj_files = [obj_files[23]]

# test run
save_folder = "./3DErrorVolumeTif" # output folder
obj_files = ["./200113plc1p2_185_segCell_uni_error.obj"]

# change light
light = bpy.data.objects["Light"].data
light.type = "SPOT"

# change camera
camera = bpy.data.objects["Camera"]
camera.location = [2.97526 , -2.39054, 1.68241] 
camera.rotation_euler = [radians(67.4201), radians(0), radians(50.89975)]

for obj_file in obj_files:
    file_loc = obj_file
    embryo_name = os.path.basename(file_loc).split('.')[0]
    
    # select mesh objects
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
        else:
            o.select_set(False)   
    bpy.ops.object.delete()

    
    import_object = bpy.ops.import_scene.obj(filepath = file_loc)
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
        else:
            o.select_set(False)			
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
    bpy.context.object.scale = [0.027, 0.027, 0.027]
    bpy.context.object.rotation_euler = [radians(-171.387), radians(0.517644), radians(88.1202)]
    bpy.context.scene.world.color = (1, 1, 1)
    bpy.context.scene.render.resolution_x = 1080

    # change camera
    # camera = bpy.data.cameras['Camera']
    # camera.angle = 0.9
    # camera.angle_x = 0.9
    # camera.angle_y = 0.6


    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    bpy.data.scenes["Scene"].render.filepath = os.path.join(save_folder, embryo_name + ".jpg")
    bpy.ops.render.render(write_still=True)
 