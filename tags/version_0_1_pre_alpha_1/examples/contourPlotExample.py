# Copyright (C) 2004 Paul Cochrane
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# $Id$

## @file contourPlotExample.py

"""
Example of plotting with pyvisi 

Will hopefully help me write a decent interface.
"""

import sys
sys.path.append('../')

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

    # create a ContourPlot object
    plot = ContourPlot(scene)

    # add the plot to the scene (really don't think I should have to do this)
    scene.add(plot)

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

    plot.render()  # need to tell some renderers to finish up stuff here

    # render the scene to screen
    scene.render(pause=True, interactive=True)

elif method == 'gnuplot':
    #### original gnuplot code
    
    import Gnuplot

    # set the plot up
    _gnuplot = Gnuplot.Gnuplot()
    _gnuplot.title('Example contour plot')
    _gnuplot.xlabel('x')
    _gnuplot.ylabel('y')
    #_gnuplot.zlabel('z')

    # this is a contour plot, so...
    _gnuplot('set contour base')
    _gnuplot('set view 0, 0, 1, 1')
    _gnuplot('set nosurface')

    # set up the data
    _data = Gnuplot.GridData(z,x,y, binary=1)

    _gnuplot.splot(_data)

    raw_input('Press enter to continue...')

elif method == 'vtk':
    pass

else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:
