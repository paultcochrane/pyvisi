# $Id$

"""
Example of plotting surfaces with pyvisi 

Will hopefully help me write a decent interface.
"""

import sys

# what plotting method are we using?
method = 'pyvisi'

# set up some data to plot
from Numeric import *

# the x and y axes
x = arange(-2,2,0.2, typecode=Float)
y = arange(-2,3,0.2, typecode=Float)

# pick some interesting function to generate the data in the third dimension
# this is the one used in the matlab docs: z = x*exp(-x^2-y^2)
z = zeros((len(x),len(y)), typecode=Float)

# boy do *I* feel old fashioned writing it this way
# surely there's another way to do it: - something to do later
for i in range(len(x)):
    for j in range(len(y)):
	z[i,j] = x[i]*exp(-x[i]*x[i] - y[j]*y[j])

# plot it with either gnuplot, vtk or pyvisi
if method == 'pyvisi':
    #### pyvisi version of code

    # import the general pyvisi stuff
    from pyvisi import *
    # import the gnuplot overrides of the interface
    from pyvisi.renderers.gnuplot import *

    # define a scene object
    # a Scene is a container for all of the kinds of things you want to put
    # into your plot, for instance, images, meshes, arrow/vector/quiver
    # plots, contour plots, spheres etc.
    scene = Scene()

    # create a SurfacePlot object
    plot = SurfacePlot(scene)

    # add some helpful info to the plot
    plot.title = 'Example surface plot'
    plot.xlabel = 'x'
    plot.ylabel = 'y'

    # assign the data to the plot
    # this version assumes that we have x, then y, then z and that z is 2D
    # and that x and y are 1D arrays
    plot.setData(x,y,z)
    # alternative syntax
    #plot.setData(xData=x, yData=y, zData=z)
    # or (but more confusing depending upon one's naming conventions)
    #plot.setData(x=x, y=y, z=z)

    # render the scene to screen
    scene.render(pause=True, interactive=True)

    # save the scene to file
    scene.save(fname="surfacePlotExample.png", format=PngImage())
    scene.save(fname="surfacePlotExample.ps", format=PsImage())

elif method == 'gnuplot':
    #### original gnuplot code
    
    import Gnuplot

    # set the plot up
    _gnuplot = Gnuplot.Gnuplot()
    _gnuplot.title('Example surface plot')
    _gnuplot.xlabel('x')
    _gnuplot.ylabel('y')
    #_gnuplot.zlabel('z')

    # this is a surface plot, so...
    _gnuplot('set surface')

    # set up the data
    _data = Gnuplot.GridData(z,x,y, binary=0)

    _gnuplot.splot(_data)

    raw_input('Press enter to continue...')

elif method == 'vtk':
    print "vtk surface plotting not yet implemented"

else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4: