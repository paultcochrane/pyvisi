# $Id$

"""
Example of plotting a vector field with pyvisi 

This example uses 2D array inputs, which is sometimes easier for users.
"""

import sys
numArgs = len(sys.argv)
if numArgs == 1:
    ren_mod = "vtk"
else:
    ren_mod = sys.argv[1]

# set up some data to plot
from Numeric import *

dim = 10

# initialise the positions of the vectors
x = zeros((dim,dim), typecode=Float)
y = zeros((dim,dim), typecode=Float)

# initialise the vector displacements
# (I may need to rethink how this works in the interface)
dx = zeros((dim,dim), typecode=Float)
dy = zeros((dim,dim), typecode=Float)

# set the positions randomly, and set the displacements to some smaller
# random number but of mean zero instead of distributed between 0 and 1
import random
random.seed()
for i in range(dim):
    for j in range(dim):
        x[i,j] = random.random()
        y[i,j] = random.random()
        dx[i,j] = (random.random()-0.5)/5.0
        dy[i,j] = (random.random()-0.5)/5.0

# example code for how a user would write a script in pyvisi
from pyvisi import *          # base level visualisation stuff
#from pyvisi.utils import *   # pyvisi specific utils
# import the objects to render the scene using the specific renderer
if ren_mod == "vtk":
    from pyvisi.renderers.vtk import *
elif ren_mod == "gnuplot":
    from pyvisi.renderers.gnuplot import *
else:
    raise ValueError, "Unknown renderer module"

# define the scene object
# a Scene is a container for all of the kinds of things you want to put 
# into your plot for instance, images, meshes, arrow plots, 
# contour plots, spheres etc.
scene = Scene()

# create a LinePlot object
plot = ArrowPlot(scene)

# add some helpful info to the plot
plot.title = 'Example 2D arrow/quiver/vector field plot'
plot.xlabel = 'x'
plot.ylabel = 'y'

# assign some data to the plot
plot.setData(x, y, dx, dy)

# render the scene to screen
scene.render(pause=True, interactive=True)

# save the scene out to file
plot.setData(x, y, dx, dy) # have to do this now because we've already
                        # render()ed the scene.  This requirement
                        # will be removed in the future
scene.save(fname="arrowPlot2D.png", format=PngImage())
    
# vim: expandtab shiftwidth=4:
