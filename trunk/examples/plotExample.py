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
y = x**2

# plot it using one of the two methods
if method == 'pyvisi':

    # example code for how a user would write a script in pyvisi
    from pyvisi import *          # base level visualisation stuff
    #from pyvisi.utils import *   # pyvisi specific utils
    # import the objects to render the scene using the specific renderer
    #from pyvisi.renderers.gnuplot import *   # gnuplot
    from pyvisi.renderers.vtk import *       # vtk
    
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
    plot.render()  # need to tell some renderers to finish up stuff here

    # render the scene to screen
    scene.render(pause=True,interactive=True)

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

    # do a quick check to make sure x and y are same length
    if len(x) != len(y):
        raise DataError, "x and y vectors must be same length"

    # set up the x and y data arrays to be able to accept the data (code
    # here adapted from the C++ of a vtk-users mailing list reply by Sander
    # Niemeijer)
    _xData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)
    _xData.SetNumberOfTuples(len(x))

    _yData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)
    _yData.SetNumberOfTuples(len(y))

    # put the data into the data arrays
    for i in range(len(x)):
        _xData.SetTuple1(i,x[i])
        _yData.SetTuple1(i,y[i])

    # create a field data object 
    # (I think this is as a containter to hold the data arrays)
    _fieldData = vtk.vtkFieldData()
    _fieldData.AllocateArrays(2)
    _fieldData.AddArray(_xData)
    _fieldData.AddArray(_yData)

    # now put the field data object into a data object so that can add it as
    # input to the xyPlotActor
    _dataObject = vtk.vtkDataObject()
    _dataObject.SetFieldData(_fieldData)

    # set up the actor
    _plot = vtk.vtkXYPlotActor()
    _plot.AddDataObjectInput(_dataObject)

    # set the title and stuff
    _plot.SetTitle("Example 2D plot")
    _plot.SetXTitle("x")
    _plot.SetYTitle("x^2")
    _plot.SetXValuesToValue()

    # set which parts of the data object are to be used for which axis
    _plot.SetDataObjectXComponent(0,0)
    _plot.SetDataObjectYComponent(0,1)

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

