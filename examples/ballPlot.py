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
Example of plotting spheres with pyvisi 
"""

import sys
numArgs = len(sys.argv)
if numArgs == 1:
    ren_mod = "vtk"
else:
    ren_mod = sys.argv[1]

import random

# set up some data to plot
from numpy import *

# the three axes in space
# this will give us 10 particles (_not_ 1000)
x = arange(10, dtype=floating)
y = arange(10, dtype=floating)
z = arange(10, dtype=floating)

# 3D position information
posArray = []
for i in range(len(x)):
    for j in range(len(y)):
        for k in range(len(z)):
            posArray.append( (x[i], y[j], z[k]) )

# radius information
random.seed()
radiiArray = zeros(len(x)*len(y)*len(z), dtype=floating)
for i in range(len(x)*len(y)*len(z)):
    radiiArray[i] = random.random()*0.8

# tag information
random.seed()
tagsArray = zeros(len(x)*len(y)*len(z), dtype=integer)
for i in range(len(x)*len(y)*len(z)):
    tagsArray[i] = int(random.random()*10)

# example code for how a user would write a script in pyvisi
from pyvisi import *          # base level visualisation stuff
# import the objects to render the scene using the specific renderer
if ren_mod == "vtk":
    from pyvisi.renderers.vtk import *       # vtk
elif ren_mod == "povray":
    from pyvisi.renderers.povray import *       # povray
else:
    raise ValueError, "Unknown renderer module"

# define the scene object
# a Scene is a container for all of the kinds of things you want to put 
# into your plot for instance, images, meshes, arrow/vector/quiver plots, 
# contour plots, spheres etc.
scene = Scene()

# create a BallPlot object
plot = BallPlot(scene)

# add some helpful info to the plot
plot.title = 'Example ball plot'

# assign some data to the plot
# one way of doing it
# (tags indirectly determine colour of the spheres in the plot)
plot.setData(points=posArray, radii=radiiArray, tags=tagsArray)

# render the scene
scene.render(pause=True, interactive=True)

# without specifying a tags array input
plot.setData(points=posArray, radii=radiiArray)
# render the scene
scene.render(pause=True, interactive=True)

# another way loading an old style-vtk file
plot.setData(fname="cp_test_0.vtk", 
	format="vtk", 
	radii="radius", 
	tags="particleTag")

# render the scene to screen
scene.render(pause=True, interactive=True)

# another way loading a vtk xml file
plot.setData(fname="cp_test_0.xml", 
	format="vtk-xml", 
	radii="radius", 
	tags="particleTag")

# render the scene to screen
scene.render(pause=True, interactive=True)

# save the scene out to file
scene.save(fname="ballPlot.png", format="png")

# vim: expandtab shiftwidth=4:

