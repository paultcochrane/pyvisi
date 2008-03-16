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

# $Id$ 
"""
Example of plotting multiple curves offset from each other with pyvisi 

This is an example with simulated seismic data, and is a larger dataset
than seismicOffsetPlotExample.py
"""

import sys
numArgs = len(sys.argv)
if numArgs == 1:
    ren_mod = "vtk"
else:
    ren_mod = sys.argv[1]

# set up some data to plot
from Numeric import *

# read in the data (being fortunate we know how much data there is)
fp = open('waves.dat')
t = zeros((100), typecode=Float)
x = zeros((13), typecode=Float)
data = zeros((100,13), typecode=Float)
for i in range(100):
    for j in range(13):
        line = fp.readline()
        arr = line.split()
        t[i] = float(arr[0])
        x[j] = float(arr[1])
        data[i,j] = float(arr[2])
fp.close()

# example code for how a user would write a script in pyvisi
from pyvisi import *          # base level visualisation stuff
#from pyvisi.utils import *   # pyvisi specific utils
# import the objects to render the scene using the specific renderer
if ren_mod == "gnuplot":
    from pyvisi.renderers.gnuplot import *   # gnuplot
elif ren_mod == "vtk":
    from pyvisi.renderers.vtk import *       # vtk
else:
    raise ValueError, "Unknown renderer module"

# define the scene object
# a Scene is a container for all of the kinds of things you want to put 
# into your plot for instance, images, meshes, arrow/vector/quiver plots, 
# contour plots, spheres etc.
scene = Scene()

# create an OffsetPlot object
plot = OffsetPlot(scene)

# add some helpful info to the plot
plot.title = 'OffsetPlot example - waves.dat'
plot.xlabel = 't'
plot.ylabel = 'y'

# assign some data to the plot
plot.setData(t, data)

# render the scene to screen
scene.render(pause=True, interactive=True)

# save the scene to file
scene.save(fname="offsetPlot.png", format=PngImage())

# vim: expandtab shiftwidth=4:

