<h1 align="center">IO tools for biomedical images</h1>
A collection of tools for processing biological or medical images.

<!-- toc -->
- [3D Segmentation Rendering](#3D-segmentation-render)
- [Overlap heatmap color](#Overlay-Heatmap)
<!-- tocstop -->

## 3D Segmentation Render
<p align="justify"> This section includes steps with which we render the 3D segmentation results of [CShaper](https://www.nature.com/articles/s41467-020-19863-x).
This is a customized framework to display our work but it maybe also valuable for showing other kinds of data.</p>

<p align="justify"> Generally speaking, multiple softwares or applications are involved in rendering the result. The data flow
 follows `*.nii.gz` --> "*.tif" --> "*.obi"/"*.mtl" --> "*.png", Specifically, </p>

1. Save segmentation (here `*.nii.gz`) as indexed tiff image. (Code: [`save_indexed_tif`](./utils/utils.py)) 

2. <p align="justify"> Use [Fiji](https://fiji.sc) plugin to extract 3D framework (`*.obi`) of the segmentation. If only one image needs to be be processed, the segmentation can be manually import and rendered with `Plugins|Process|Show color surface`; If a bunch  of images are required, the `Macros` would be helpful. (Code: [`draw3DSnap.ijm`](./draw3DSnap.ijm))</p>
3. <p align="justify"> The [blender](https://www.blender.org) can import `*.obj` and even support user defined python script. Also, the python script can be used to process multiple images automatically. (Code: [blender script](./utils/blender_render.py))</p> 

## Overlay Heatmap
A transparent color map is overlaied on the raw image. For details, please refer to [HeatMap](https://github.com/LinShanify/HeatMap). (Code: [`Heatmap.py`](./utils/heatmap.py))

