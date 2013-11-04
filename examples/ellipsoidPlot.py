# Copyright (C) 2004-2008 Paul Cochrane
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


"""
Example of plotting ellipsoids (useful for visualising tensors) with pyvisi 
"""

import sys
numArgs = len(sys.argv)
if numArgs == 1:
    ren_mod = "vtk"
else:
    ren_mod = sys.argv[1]

# set up some data to plot
from numpy import *

# example code for how a user would write a script in pyvisi
from pyvisi import *          # base level visualisation stuff
# import the objects to render the scene using the specific renderer

if ren_mod == "vtk":
    from pyvisi.renderers.vtk import *       # vtk
elif ren_mod == "povray":
    from pyvisi.renderers.povray import *    # povray
else:
    raise ValueError, "Unknown renderer module"

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
scene.save(fname="ellipsoidPlot.png", format="png")

# vim: expandtab shiftwidth=4:

