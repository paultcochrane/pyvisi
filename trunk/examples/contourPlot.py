# $Id$

"""
Example of contour plotting with pyvisi 
"""

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
    #from pyvisi.renderers.gnuplot import *
    from pyvisi.renderers.vtk import *

    # define a scene object
    # a Scene is a container for all of the kinds of things you want to put
    # into your plot, for instance, images, meshes, arrow/vector/quiver
    # plots, contour plots, spheres etc.
    scene = Scene()

    # create a ContourPlot object
    plot = ContourPlot(scene)

    # add some helpful info to the plot
    plot.title = 'Example contour plot'
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
    plot.setData(x,y,z)  # have to do this now because we've already
                         # render()ed the scene.  This requirement will be
                         # removed in the future
    scene.save(fname="contourPlot.png", format=PngImage())

elif method == 'plplot':

    import plplot

    # determine the min and max of x
    xMin = min(x)
    xMax = max(x)
    
    yMin = min(y)
    yMax = max(y)
    
    plplot.plsdev("xwin")
    plplot.plinit()
    plplot.plenv(xMin, xMax, yMin, yMax, 0, 1)
    plplot.pllab("x", "y", "Example shaded contour plot")
    plshades(zz, shedge, fill_width, 1, pltr1, xg1, yg1)

    zmin = min(zz.flat)
    zmax = max(zz.flat)

    clevel = zmin + (zmax - zmin) * (arrayrange(NS)+0.5)/NS
    shedge = zmin + (zmax - zmin) * (arrayrange(NS+1))/NS

    plplot.plend()
    
    # to save as well, have to set everything up again, and replot
    # save as png
    plplot.plsdev("png")
    plplot.plsfnam("contourPlot.png")
    plplot.plinit()
    plplot.plenv(xMin, xMax, yMin, yMax, 0, 1)
    plplot.pllab("x", "y", "Example shaded contour plot")
    plplot.plline(x, y1)
    plplot.plend()
else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:
