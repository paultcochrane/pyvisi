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
method = 'vtk'

# set up some data to plot
from Numeric import *

x = arange(10, typecode=Float)
y = x**2

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
    plot.setData(x,y)

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
    _data = Gnuplot.Data(x, y, with='lines')

    # plot it
    _gnuplot.plot(_data)

    raw_input('Press enter to continue...\n')

elif method == 'vtk':
    #### original vtk code

    import vtk

    # set up the renderer and the render window
    _ren = vtk.vtkRenderer()
    _renWin = vtk.vtkRenderWindow()
    _renWin.AddRenderer(_ren)
    _ren.SetBackground(1,1,1)
    _renWin.SetSize(600,600)

    # copy the data into vtk data objects
    _x = vtk.vtkDoubleArray()
    _x.SetName("x")
    for i in range(len(x)):
        _x.InsertNextValue(x[i])

    _xData = vtk.vtkRectilinearGrid()
    _xData.SetDimensions(len(x),1,1)
    _xData.SetXCoordinates(_x)
    # fundamental point: must set the points within the data, beforehand had
    # only set up structural info.  So, must use SetScalars()
    _xData.GetPointData().SetScalars(_x)

    # and now for the y data
    _y = vtk.vtkDoubleArray()
    _y.SetName("y")
    for i in range(len(y)):
        _y.InsertNextValue(y[i])

    _yData = vtk.vtkRectilinearGrid()
    _yData.SetDimensions(len(y),1,1)
    _yData.SetXCoordinates(_y)
    _yData.GetPointData().SetScalars(_y)

    # set up the actor
    _plot = vtk.vtkXYPlotActor()
    _plot.AddInput(_xData)
    _plot.AddInput(_yData)

    # set the title and stuff
    _plot.SetTitle("Example 2D plot")
    _plot.SetXTitle("x")
    _plot.SetYTitle("x^2")
    _plot.GetProperty().SetColor(0,0,0)
    _plot.GetProperty().SetLineWidth(2)
    print _plot
    print _plot.GetPointComponent(1)
    _plot.SetPointComponent(0,0)
    _plot.SetXValuesToValue()
    #print _plot
    #print _plot.GetInputList()
    #print _yData.GetPoint(2)
    #print _xData.GetPoint(2)
    #print _yData.GetNumberOfPoints()
    print _plot.GetXValues()

    # add the actor
    _ren.AddActor2D(_plot)
    
    # render the scene
    _iren = vtk.vtkRenderWindowInteractor()
    _iren.SetRenderWindow(_renWin)
    _iren.Initialize()
    _renWin.Render()
    _iren.Start()

    # pause for input
    #raw_input('Press enter to continue...\n')

else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:

