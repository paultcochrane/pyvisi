# $Id$ 
"""
Example of plotting multiple curves offset from each other with pyvisi 

This is an example with simulated seismic data
"""

import sys
numArgs = len(sys.argv)
if numArgs == 1:
    ren_mod = "vtk"
else:
    ren_mod = sys.argv[1]

# set up some data to plot
from Numeric import *

# read in the data (being fortunate we know how much data there is)
fp = open('waves.dat')
t = zeros((100), typecode=Float)
x = zeros((13), typecode=Float)
data = zeros((100,13), typecode=Float)
for i in range(100):
    for j in range(13):
        line = fp.readline()
        arr = line.split()
        t[i] = float(arr[0])
        x[j] = float(arr[1])
        data[i,j] = float(arr[2])
fp.close()

# example code for how a user would write a script in pyvisi
from pyvisi import *          # base level visualisation stuff
#from pyvisi.utils import *   # pyvisi specific utils
# import the objects to render the scene using the specific renderer
if ren_mod == "gnuplot":
    from pyvisi.renderers.gnuplot import *   # gnuplot
elif ren_mod == "vtk":
    from pyvisi.renderers.vtk import *       # vtk
else:
    raise ValueError, "Unknown renderer module"

# define the scene object
# a Scene is a container for all of the kinds of things you want to put 
# into your plot for instance, images, meshes, arrow/vector/quiver plots, 
# contour plots, spheres etc.
scene = Scene()

# create a LinePlot object
plot = LinePlot(scene)

# add some helpful info to the plot
plot.title = 'Sample seismic data'
plot.xlabel = 't'
plot.ylabel = 'y'

plot.linestyle = 'lines'

# assign some data to the plot
plot.setData(t, data[:,0], data[:,1], data[:,2], data[:,3], 
        data[:,4], data[:,5], data[:,6], data[:,7], data[:,8],
        data[:,9], data[:,10], data[:,11], data[:,12], offset=True)

# render the scene to screen
scene.render(pause=True, interactive=True)

# save the scene to file
scene.save(fname="seismicOffsetPlot1.png", format=PngImage())

# vim: expandtab shiftwidth=4:
