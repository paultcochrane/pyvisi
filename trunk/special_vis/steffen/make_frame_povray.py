#!/usr/bin/env python

"""
Make a movie frame from an LSM simulation vtk xml data file
This time use povray as the renderer, but use vtk to extract the data
from the data file
"""

import vtk
import os, sys, re
import getopt
from math import *
from Numeric import *

(opts, args) = getopt.getopt(sys.argv[1:],
	"d:f:i:o:s:n:t:r",
	["dirname=", 
	"fname=", 
	"index=", 
	"outdir=", 
	"outfname=",
	"numframes=", 
	"tagindex=", 
	"rotate",
	],
	)

dirname = None
fname = None
index = None
outdir = None
outFnameStem = None
numframes = None
opaqueTagIndex = None
rotate = False

for option, arg in opts:
    if option in ('-d', '--dirname'):
	dirname = arg
	print "Input arg: dirname = %s" % dirname
    elif option in ('-f', '--fname'):
	fname = arg
	print "Input arg: fname = %s" % fname
    elif option in ('-i', '--index'):
	index = int(arg)
	print "Input arg: index = %d" % index
    elif option in ('-o', '--outdir'):
	outdir = arg
	print "Input arg: outdir = %s" % outdir
    elif option in ('-s', '--outfname'):
	outFnameStem = arg
	print "Input arg: outFnameStem = %s" % outFnameStem
    elif option in ('-n', '--numframes'):
	numframes = int(arg)
	print "Input arg: numframes = %d" % numframes
    elif option in ('-t', '--tagindex'):
	opaqueTagIndex = int(arg)
	print "Input arg: opaqueTagIndex = %d" % opaqueTagIndex
    elif option in ('-r', '--rotate'):
	print "Input arg: rotate True"
	rotate = True

if dirname is None:
    raise ValueError, "You must supply a directory name (of the xml files)"
if fname is None:
    raise ValueError, "You must supply a file name (of the frame)"
if index is None:
    raise ValueError, "You must supply an index for the frame"
if outdir is None:
    raise ValueError, "You must supply an output directory for the frames"
if numframes is None:
    raise ValueError, "You must supply the maximum number of frames"

# resolution to use: 
# low = 640x480
# med = 800x600
# high = 1024x768
res = "med"

def makeFrame(dirname, fname, index, outdir, outFnameStem, numframes, opaqueTagIndex, rotFlag):
    """
    Generate image from xml file in given file (complete path possible), and
    output image in current directory
    """
    rotate = rotFlag
    rotPoint = 90   # after this many frames start rotating about the model
    
    # if we have been given a stem for the image filename, use it, otherwise
    # autogenerate it from the stem of the xml file
    if outFnameStem is not None:
	imgFnameStem = outFnameStem
    else:
	# grab the stem of the xml file and use as the stem of the image filename
	r = re.compile(r"_\d+\.\w+$")
	imgFnameStem = r.sub('',fname)
    
    # create the reader of the file
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(dirname+'/'+fname)
    reader.Update()
    
    # read the output into an unstructured grid (automatically instantiated 
    # from the call to the reader)
    grid = reader.GetOutput()

    modelCentre = grid.GetCenter()

    # grab the points
    vtkPoints = grid.GetPoints()

    # grab the radii and the tag data
    vtkRadii = grid.GetPointData().GetScalars("radius")
    vtkTags = grid.GetPointData().GetScalars("particleTag")

    # now try and work out how many tags there are so that can work out
    # what the relevant scalar range should be
    numPoints = vtkTags.GetNumberOfTuples()
    valueDict = {}
    for i in range(numPoints):
	tagValue = vtkTags.GetValue(i)
	valueDict[tagValue] = 1

    numTags = len(valueDict.keys())

    tagValues = valueDict.keys()
    tagValues.sort()

    # count the number of tags, and make an evenly spaced array of points
    # between zero and one, then use these as the scalars to colour by
    vtkMappedTags = vtk.vtkFloatArray()
    vtkMappedTags.SetNumberOfTuples(numPoints)
    vtkMappedTags.SetNumberOfComponents(1)
    vtkMappedTags.SetName("tags")
    for i in range(numPoints):
	tagValue = vtkTags.GetValue(i)
	for j in range(numTags):
	    if tagValue == tagValues[j]:
		vtkMappedTags.InsertTuple1(i, float(j)/float(numTags-1))

    # make the lookup table, and set all tags translucent bar one
    lut = vtk.vtkLookupTable()
    lut.Build()

    # grab the rgb values for the mapped tags values
    red = zeros(numPoints, typecode=Float)
    green = zeros(numPoints, typecode=Float)
    blue = zeros(numPoints, typecode=Float)
    for i in range(numPoints):
	#red[i], green[i], blue[i] = lut.GetColor(vtkMappedTags.GetValue(i))
	rgb = zeros(3, typecode=Float)
	lut.GetColor(vtkMappedTags.GetValue(i), rgb)
	red[i] = rgb[0]
	green[i] = rgb[1]
	blue[i] = rgb[2]

    # now convert the information we want (radii, colours, positions) into
    # array objects so that I can play with them as per normal in python

    ### the points, the radii and the tags
    x = zeros(numPoints, typecode=Float)
    y = zeros(numPoints, typecode=Float)
    z = zeros(numPoints, typecode=Float)
    radii = zeros(numPoints, typecode=Float)
    mappedTags = zeros(numPoints, typecode=Float)
    tags = zeros(numPoints, typecode=Float)
    for i in range(numPoints):
	x[i], y[i], z[i] = vtkPoints.GetPoint(i)
	radii[i] = vtkRadii.GetValue(i)
	mappedTags[i] = vtkMappedTags.GetValue(i)
	tags[i] = vtkTags.GetValue(i)

    ### generate the pov file

    # open the pov file to write to
    pov = open("%s/%s_%04d.pov" % (outdir, imgFnameStem, index) , "w")

    # version information
    pov.write("#version 3.5;\n")

    # the include files to add
    pov.write("#include \"shapes.inc\"\n")
    pov.write("#include \"colors.inc\"\n")

    pov.write("global_settings {\n")
    pov.write("  max_trace_level 256\n")
    pov.write("}\n")

    # the camera
    pov.write("camera {\n")
    pov.write("  location <%f, %f, -100>\n" % 
	    (modelCentre[0], modelCentre[1])) # need to work out z dynamically
    # the up and right used here are actually the pov defaults
    pov.write("  up <0, 1, 0>\n")  # up is in y direction
    pov.write("  right <4/3, 0, 0>\n") 
    pov.write("  look_at <%f, %f, -%f>\n" %
	    (modelCentre[0], modelCentre[1], modelCentre[2]))
    pov.write("}\n")

    # the light source
    pov.write("light_source {\n")
    pov.write("  <%f, %f, -300>\n" % (modelCentre[0], modelCentre[1]))
    pov.write("  colour White\n")
    pov.write("}\n")

    # use an infinite plane as the background
    pov.write("plane { <0, 0, -1>, -100\n")
    pov.write("  pigment {\n")
    pov.write("    colour White\n")
    pov.write("  }\n")
    pov.write("}\n")

    # the spheres
    for i in range(numPoints):
	pov.write("sphere {\n")
	pov.write("  <%f, %f, -%f>, %f\n" %
		(x[i], y[i], z[i], radii[i]))
	pov.write("  pigment {\n")
	if opaqueTagIndex is not None:
	    for j in range(numTags):
		if tagValues[j] == opaqueTagIndex:
		    tagValueIndex = j
	    if tags[i] == tagValueIndex:
		pov.write("    colour red %f green %f blue %f\n" %
			(red[i], green[i], blue[i]))
	    else:
		pov.write("    rgbt <%f, %f, %f, 0.95>\n" %
			(red[i], green[i], blue[i]))
	else:
	    pov.write("    colour red %f green %f blue %f\n" %
		    (red[i], green[i], blue[i]))
	pov.write("  }\n")
	pov.write("}\n")

    # close the file
    pov.close()


    ### generate the ini file

    # open the ini file
    ini = open("%s/%s_%04d.ini" % (outdir, imgFnameStem, index), "w")

    # the output resolution
    if res == "low":
	resX = 640
	resY = 480
    elif res == "med":
	resX = 800
	resY = 600
    elif res == "high":
	resX = 1024
	resY = 768
    ini.write("Width=%f\n" % resX)
    ini.write("Height=%f\n" % resY)

    # turn the display off
    ini.write("Display=off\n")

    # anti-aliasing settings
    ini.write("Antialias=on\n")

    # generate compressed TGA files
    ini.write("Output_File_Type=C\n")

    # the name of the input pov file
    ini.write("Input_File_Name=%s/%s_%04d.pov\n" %
	    (outdir, imgFnameStem, index))

    # pause when done?
    ini.write("Pause_When_Done=off\n")

    # close the file
    ini.close()

    ### run povray on the file
    cmd = "povray %s/%s_%04d.ini" % (outdir, imgFnameStem, index)
    os.system(cmd)

    # status information
    print "    Wrote %s_%04d.tga" % (imgFnameStem, index)

    # convert the file to ppm format with tgatoppm (for later processing
    # with ppmtompeg)
    #cmd = "tgatoppm %s_%04d.tga > %s_%04d.ppm" % \
	    #(imgFnameStem, index, imgFnameStem, index)
    #os.system(cmd)

    # status information
    #print "    Wrote %s_%04d.ppm" % (imgFnameStem, index)

    
# do it
makeFrame(dirname, fname, index, outdir, outFnameStem, numframes, opaqueTagIndex, rotate)

