# $Id$

"""
Example of plotting a curve using only one input array with pyvisi 

Will hopefully help me write a decent interface.
"""

import sys

# what plotting method are we using?
method = 'pyvisi'

# set up some data to plot
from Numeric import *

x = arange(0,2*pi,0.1, typecode=Float)
y = sin(x)

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
    plot.xlabel = 'index'
    plot.ylabel = 'y'

    plot.linestyle = 'lines'
    
    # assign some data to the plot
    plot.setData(y)

    # render the scene to screen
    scene.render(pause=True,interactive=True)

    # save the scene to file
    #scene.save(fname="singleArrayPlotExample.png", format=PngImage())
    #scene.save(fname="singleArrayPlotExample.ps", format=PsImage())

elif method == 'gnuplot':
    #### original gnuplot code
    
    import Gnuplot

    # set the plot up
    _gnuplot = Gnuplot.Gnuplot()
    _gnuplot.title('Example 2D plot')
    _gnuplot.xlabel('index')
    _gnuplot.ylabel('y')

    # set up the data
    _data = Gnuplot.Data(y, with='lines')

    # plot it
    _gnuplot.plot(_data)

    # save it to file
    _gnuplot('set terminal png')
    _gnuplot('set output "singleArrayPlotExample.png"')
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
        raise ValueError, "x and y vectors must be same length"

    # set up the x and y data arrays to be able to accept the data (code
    # here adapted from the C++ of a vtk-users mailing list reply by Sander
    # Niemeijer)
    _xData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)
    _xData.SetNumberOfTuples(len(y))

    _yData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)
    _yData.SetNumberOfTuples(len(y))

    # put the data into the data arrays
    for i in range(len(x)):
        _xData.SetTuple1(i,i+1)
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
    _plot.SetXTitle("index")
    _plot.SetYTitle("y")
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

    # convert the render window to an image
    _win2imgFilter = vtk.vtkWindowToImageFilter()
    _win2imgFilter.SetInput(_renWin)

    # save the image to file
    _outWriter = vtk.vtkPNGWriter()
    _outWriter.SetInput(_win2imgFilter.GetOutput())
    _outWriter.SetFileName("singleArrayPlotExample.png")
    _outWriter.Write()

    # pause for input
    #raw_input('Press enter to continue...\n')

else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:

