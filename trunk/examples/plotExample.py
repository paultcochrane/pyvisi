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

## @file basicExample.py

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

x = arange(10, typecode=Float)
y1 = x**2

# plot it using one of the two methods
if method == 'pyvisi':

    # example code for how a user would write a script in pyvisi
    from pyvisi import *          # base level visualisation stuff
    #from pyvisi.utils import *   # pyvisi specific utils
    # import the objects to render the scene using gnuplot
    from pyvisi.renderers.gnuplot import * 
    
    # define the scene object
    # a Scene is a container for all of the kinds of things you want to put 
    # into your plot for instance, images, meshes, arrow/vector/quiver plots, 
    # contour plots, spheres etc.
    scene = Scene()
    
    # create a LinePlot object
    plot = LinePlot(scene)
    
    # add the plot to the scene
    scene.add(plot)

    # add some helpful info to the plot
    plot.title = 'Example 2D plot'
    plot.xlabel = 'x'
    plot.ylabel = 'x^2'

    plot.linestyle = 'lines'
    
    # assign some data to the plot
    plot.setData(x,y1)

    # render the scene to screen
    scene.render(pause=True)

elif method == 'gnuplot':
    #### original gnuplot code
    
    import Gnuplot

    # set the plot up
    _gnuplot = Gnuplot.Gnuplot()
    _gnuplot.title('Example 2D plot')
    _gnuplot.xlabel('x')
    _gnuplot.ylabel('x^2')

    # set up the data
    _data = Gnuplot.Data(x, y1, with='lines')

    # plot it
    _gnuplot.plot(_data)

    raw_input('Press enter to continue...\n')

elif method == 'vtk':
    #### original vtk code

    import vtk

    # set up the renderer and the render window
    _ren = vtkRenderer()
    _renWin = vtkRenderWindow()
    _renWin.AddRenderer(_ren)
    
    # render the scene
    _renWin.Render()

    # pause for input
    raw_input('Press enter to continue...\n')

else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:

