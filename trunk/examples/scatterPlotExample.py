# $Id$

"""
Example of a scatter plot in pyvisi 

Will hopefully help me write a decent interface.
"""

import sys

# what plotting method are we using?
method = 'pyvisi'

# set up some data to plot
from Numeric import *
import random

x = arange(10, typecode=Float)
y = zeros(10, typecode=Float)
random.seed()
for i in range(len(x)):
    y[i] = random.random()

# plot it using one of the three methods
if method == 'pyvisi':

    # example code for how a user would write a script in pyvisi
    from pyvisi import *          # base level visualisation stuff
    #from pyvisi.utils import *   # pyvisi specific utils
    # import the objects to render the scene using the specific renderer
    from pyvisi.renderers.gnuplot import *   # gnuplot
    #from pyvisi.renderers.vtk import *       # vtk
    
    # define the scene object
    # a Scene is a container for all of the kinds of things you want to put 
    # into your plot for instance, images, meshes, arrow/vector/quiver plots, 
    # contour plots, spheres etc.
    scene = Scene()
    
    # create a ScatterPlot object
    plot = ScatterPlot(scene)
    
    # add some helpful info to the plot
    plot.title = 'Example 2D scatter plot'
    plot.xlabel = 'x'
    plot.ylabel = 'y'

    # assign some data to the plot
    plot.setData(x, y)

    # render the scene to screen
    scene.render(pause=True, interactive=True)

    # save the scene out to file
    scene.save(fname="scatterPlotExample.png", format=PngImage())
    scene.save(fname="scatterPlotExample.ps", format=PsImage())

elif method == 'gnuplot':
    #### original gnuplot code
    
    import Gnuplot

    # set the plot up
    _gnuplot = Gnuplot.Gnuplot()
    _gnuplot.title('Example 2D scatter plot')
    _gnuplot.xlabel('x')
    _gnuplot.ylabel('y')

    # set up the data
    _data = Gnuplot.Data(x, y, with='points pointtype 2')

    # plot it
    _gnuplot.plot(_data)

    # set up to save to file
    _gnuplot('set terminal png')
    _gnuplot('set output \"scatterPlotExample.png\"')

    # save it
    _gnuplot.plot(_data)

    raw_input('Press enter to continue...\n')

elif method == 'vtk':
    #### original vtk code
    print "vtk scatter plotting not yet implemented"

else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:
