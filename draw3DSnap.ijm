input = "D:/ProjectData/CMapEvaluation/3DCShaper/tif/";
output = "D:/ProjectData/CMapEvaluation/3DCShaper/tif/";
label_path = "D:/ProjectData/CMapEvaluation/3DCShaper/3DCShaper.txt";

filestring = File.openAsString(label_path);
x = split(filestring, "\n");

//setBatchMode(true);
label_list = getFileList(input);
for (i = 0; i < label_list.length; i++){
	label = x[i];
	action(input, output, label_list[i], i, label);
    //run("Close All");
	//call("ij3d.ImageJ3DViewer.exportContent", "STL ASCII", "C:/Users/jfcao3/Desktop/untitled.stl");
	//write("finish exporting!");
//setBatchMode(false);
}


function action(input, output, filename, i, label) {
	write("Processing: " + filename);
	open(input + filename);
	name_split = split(filename, ".");
	base_name = name_split[0];
	call("ij3d.ImageJ3DViewer.setCoordinateSystem", "false");
	run("Show Color Surfaces", "use=[Create New 3D Viewer] resampling=1 index=0 radius=1");

	call("ij3d.ImageJ3DViewer.select", "Smoothed image for colour index: " + label);
	call("ij3d.ImageJ3DViewer.exportContent", "WaveFront", output + base_name + ".obj");
	//call("ij3d.ImageJ3DViewer.snapshot", "512", "512");	
	//saveAs("Jpeg", output + "snap" + i + ".jpg");
	call("ij3d.ImageJ3DViewer.close");
	run("Close All");
}