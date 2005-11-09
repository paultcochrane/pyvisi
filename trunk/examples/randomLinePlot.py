# $Id$

"""
Example of plotting lines with pyvisi 

This time using a large set of random numbers as input and can be used to
stress test the underlying renderer module.
"""

import sys
numArgs = len(sys.argv)
if numArgs == 1:
    ren_mod = "vtk"
else:
    ren_mod = sys.argv[1]

# set up some data to plot
from Numeric import *
import random

numPoints = 100000
x = arange(numPoints, typecode=Float)
y = zeros(numPoints, typecode=Float)
random.seed()
for i in range(numPoints):
    y[i] = random.random()

y2 = 2*y

# example code for how a user would write a script in pyvisi
from pyvisi import *          # base level visualisation stuff
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
plot.title = 'Example of a 2D line plot of random numbers'
plot.xlabel = 'x'
plot.ylabel = 'y'
plot.linestyle = 'lines'

# assign some data to the plot
plot.setData(range(numPoints), y)

# render the scene to screen
#scene.render(pause=True, interactive=True)
scene.save(fname="randomLinePlot1.png", format="png")

plot.title = 'Another example of a 2D line plot of random numbers'
plot.xlabel = 'x'
plot.ylabel = 'y'
plot.linestyle = 'lines'

plot.setData(range(numPoints), y2)

# save the scene out to file
scene.save(fname="randomLinePlot2.png", format="png")

# vim: expandtab shiftwidth=4:
