# $Id$

"""
Example of plotting ellipsoids (useful for visualising tensors) with pyvisi 
"""

# what plotting method are we using?
method = 'pyvisi'

# set up some data to plot
from Numeric import *

# plot it using one of the methods
if method == 'pyvisi':

    # example code for how a user would write a script in pyvisi
    from pyvisi import *          # base level visualisation stuff
    # import the objects to render the scene using the specific renderer
    from pyvisi.renderers.vtk import *       # vtk
    #from pyvisi.renderers.povray import *    # povray
    
    # define the scene object
    # a Scene is a container for all of the kinds of things you want to put 
    # into your plot for instance, images, meshes, arrow/vector/quiver plots, 
    # contour plots, spheres etc.
    scene = Scene()
    
    # create a EllipsoidPlot object
    plot = EllipsoidPlot(scene)
    
    # add some helpful info to the plot
    plot.title = 'Example ellipsoid plot'

    # plot data defined in a vtk file
    plot.setData(fname='stress22.vtk', format='vtk-xml')

    scene.render(pause=True, interactive=True)

    # save the plot
    plot.setData(fname='stress22.vtk', format='vtk-xml')

    scene.save(fname="ellipsoidPlot.png", format="png")

elif method == 'povray':
    print "Sorry, the povray interface hasn't been written yet."

else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:

