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

## @file multiCurvePlotExample.py

"""
Example of plotting multiple curves with pyvisi 

Will hopefully help me write a decent interface.
"""

import sys
sys.path.append('../')

# what plotting method are we using?
method = 'pyvisi'

# set up some data to plot
from Numeric import *

x = arange(0,2*pi,0.1, typecode=Float)
y1 = sin(x)
y2 = cos(x)
y3 = cos(x)**2

# plot it using one of the three methods
if method == 'pyvisi':

    # example code for how a user would write a script in pyvisi
    from pyvisi import *          # base level visualisation stuff
    #from pyvisi.utils import *   # pyvisi specific utils
    # import the objects to render the scene using the specific renderer
    from pyvisi.renderers.gnuplot import *   # gnuplot
    #from pyvisi.renderers.vtk import *       # vtk
    
    # define the scene object
    # a Scene is a container for all of the kinds of things you want to put 
    # into your plot for instance, images, meshes, arrow/vector/quiver plots, 
    # contour plots, spheres etc.
    scene = Scene()
    
    # create a LinePlot object
    plot = LinePlot(scene)
    
    # add some helpful info to the plot
    plot.title = 'Example 2D plot'
    plot.xlabel = 'x'
    plot.ylabel = 'y'

    plot.linestyle = 'lines'
    
    # assign some data to the plot
    plot.setData(x, y1, y2, y3)
    plot.render()  # need to tell some renderers to finish up stuff here

    # render the scene to screen
    scene.render(pause=True,interactive=True)

    # save the scene to file
    scene.save(fname="multiCurvePlotExample.png", format="PNG")
    #scene.save(fname="multiCurvePlotExample.ps", format="PS")

elif method == 'gnuplot':
    #### original gnuplot code
    
    import Gnuplot

    # set the plot up
    _gnuplot = Gnuplot.Gnuplot()
    _gnuplot.title('Example 2D plot')
    _gnuplot.xlabel('x')
    _gnuplot.ylabel('y')

    # set up the data
    _data1 = Gnuplot.Data(x, y1, with='lines')
    _data2 = Gnuplot.Data(x, y2, with='lines')
    _data3 = Gnuplot.Data(x, y3, with='lines')

    # plot it
    _gnuplot.plot(_data1, _data2, _data3)

    # save it to file
    _gnuplot('set terminal png')
    _gnuplot('set output "multiCurvePlotExample.png"')
    _gnuplot.plot(_data1, _data2, _data3)

    raw_input('Press enter to continue...\n')

elif method == 'vtk':
    #### original vtk code

    import vtk

    # set up the renderer and the render window
    _ren = vtk.vtkRenderer()
    _renWin = vtk.vtkRenderWindow()
    _renWin.AddRenderer(_ren)

    # do a quick check to make sure x and y are same length
    if len(x) != len(y1):
        raise ValueError, "x and y vectors must be same length"

    if len(x) != len(y2):
        raise ValueError, "x and y vectors must be same length"

    # set up the x and y data arrays to be able to accept the data (code
    # here adapted from the C++ of a vtk-users mailing list reply by Sander
    # Niemeijer)
    _xData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)
    _xData.SetNumberOfTuples(len(x))

    _yData1 = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)
    _yData1.SetNumberOfTuples(len(y1))

    _yData2 = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)
    _yData2.SetNumberOfTuples(len(y2))

    _yData3 = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)
    _yData3.SetNumberOfTuples(len(y3))

    # put the data into the data arrays
    for i in range(len(x)):
        _xData.SetTuple1(i,x[i])
        _yData1.SetTuple1(i,y1[i])
        _yData2.SetTuple1(i,y2[i])
        _yData3.SetTuple1(i,y3[i])

    # create a field data object 
    # (I think this is as a containter to hold the data arrays)
    _fieldData1 = vtk.vtkFieldData()
    _fieldData1.AllocateArrays(2)
    _fieldData1.AddArray(_xData)
    _fieldData1.AddArray(_yData1)

    _fieldData2 = vtk.vtkFieldData()
    _fieldData2.AllocateArrays(2)
    _fieldData2.AddArray(_xData)
    _fieldData2.AddArray(_yData2)

    _fieldData3 = vtk.vtkFieldData()
    _fieldData3.AllocateArrays(2)
    _fieldData3.AddArray(_xData)
    _fieldData3.AddArray(_yData3)

    # now put the field data object into a data object so that can add it as
    # input to the xyPlotActor
    _dataObject1 = vtk.vtkDataObject()
    _dataObject1.SetFieldData(_fieldData1)

    _dataObject2 = vtk.vtkDataObject()
    _dataObject2.SetFieldData(_fieldData2)

    _dataObject3 = vtk.vtkDataObject()
    _dataObject3.SetFieldData(_fieldData3)

    # set up the actor
    _plot = vtk.vtkXYPlotActor()
    _plot.AddDataObjectInput(_dataObject1)
    _plot.AddDataObjectInput(_dataObject2)
    _plot.AddDataObjectInput(_dataObject3)

    # set the title and stuff
    _plot.SetTitle("Example 2D plot")
    _plot.SetXTitle("x")
    _plot.SetYTitle("y")
    _plot.SetXValuesToValue()

    # set which parts of the data object are to be used for which axis
    _plot.SetDataObjectXComponent(0,0)
    _plot.SetDataObjectYComponent(0,1)
    _plot.SetDataObjectYComponent(1,1)
    _plot.SetDataObjectYComponent(2,1)

    # add the actor
    _ren.AddActor2D(_plot)
    
    # render the scene
    _iren = vtk.vtkRenderWindowInteractor()
    _iren.SetRenderWindow(_renWin)
    _iren.Initialize()
    _renWin.Render()
    _iren.Start()

    # convert the render window to an image
    _win2imgFilter = vtk.vtkWindowToImageFilter()
    _win2imgFilter.SetInput(_renWin)

    # save the image to file
    _outWriter = vtk.vtkPNGWriter()
    _outWriter.SetInput(_win2imgFilter.GetOutput())
    _outWriter.SetFileName("multiCurvePlotExample.png")
    _outWriter.Write()

    # pause for input
    #raw_input('Press enter to continue...\n')

else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:

