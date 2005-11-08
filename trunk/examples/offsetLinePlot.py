# $Id$ 
"""
Example of plotting multiple curves offset from each other with pyvisi 

This is especially handy for people plotting seismic data
"""

import sys
numArgs = len(sys.argv)
if numArgs == 1:
    ren_mod = "vtk"
else:
    ren_mod = sys.argv[1]

# set up some data to plot
from Numeric import *

x = arange(0,2*pi,0.01, typecode=Float)
y1 = sin(x)
y2 = cos(x)
y3 = cos(x)**2
y4 = sin(2*x)
y5 = cos(3*x)
y6 = sin(20*x)

# example code for how a user would write a script in pyvisi
from pyvisi import *          # base level visualisation stuff
#from pyvisi.utils import *   # pyvisi specific utils
# import the objects to render the scene using the specific renderer
if ren_mod == "gnuplot":
    from pyvisi.renderers.gnuplot import *   # gnuplot
elif ren_mod == "vtk":
    from pyvisi.renderers.vtk import *       # vtk
elif ren_mod == "plplot":
    from pyvisi.renderers.plplot import *    # plplot
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
plot.title = 'Example 2D plot with offsets'
plot.xlabel = 'x'
plot.ylabel = 'y'

plot.linestyle = 'lines'

# assign some data to the plot
plot.setData(x, y1, y2, y3, y4, y5, y6, offset=True)

# render the scene to screen
scene.render(pause=True, interactive=True)

# save the scene to file
# save as png
plot.setData(x, y1, y2, y3, y4, y5, y6, offset=True)
			     # have to do this now because we've already
			     # render()ed the scene.  This requirement
			     # will be removed in the future.
scene.save(fname="offsetLinePlot.png", format=PngImage())

# save as postscript
plot.setData(x, y1, y2, y3, y4, y5, y6, offset=True)  
			     # have to do this now because we've already
			     # save()d the scene.  This requirement will
			     # be removed in the future.
scene.save(fname="offsetLinePlot.ps", format=PsImage())

# vim: expandtab shiftwidth=4:

