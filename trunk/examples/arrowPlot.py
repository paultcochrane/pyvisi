# $Id$

"""
Example of plotting a vector field with pyvisi 
"""

# what plotting method are we using?
method = 'pyvisi'

# set up some data to plot
from Numeric import *

# the positions of the vectors
x = arange(20, typecode=Float)
y = arange(20, typecode=Float)

# the vector displacements
# (I may need to rethink how this works in the interface)
dx = arange(20, typecode=Float)
dy = arange(20, typecode=Float)

# set the positions randomly, and set the displacements to be the square of
# the positions
import random
random.seed()
for i in range(len(x)):
    x[i] = random.random()
    y[i] = random.random()
    dx[i] = x[i]*x[i]
    dy[i] = y[i]*y[i]

# plot it using one of the three methods
if method == 'pyvisi':

    # example code for how a user would write a script in pyvisi
    from pyvisi import *          # base level visualisation stuff
    # import the objects to render the scene using the specific renderer
    #from pyvisi.renderers.gnuplot import *   # gnuplot
    from pyvisi.renderers.vtk import *   # vtk
    
    # define the scene object
    # a Scene is a container for all of the kinds of things you want to put 
    # into your plot for instance, images, meshes, arrow/vector/quiver plots, 
    # contour plots, spheres etc.
    scene = Scene()
    
    # create an ArrowPlot object
    plot = ArrowPlot(scene)
    
    # add some helpful info to the plot
    plot.title = 'Example 2D arrow/quiver/vector field plot'
    plot.xlabel = 'x'
    plot.ylabel = 'y'

    # assign some data to the plot
    plot.setData(x, y, dx, dy)

    # render the scene to screen
    scene.render(pause=True, interactive=True)

    # save the scene out to file
    plot.setData(x, y, dx, dy) # have to do this now because we've already
                               # render()ed the scene.  This requirement
                               # will be removed in the future
    scene.save(fname="arrowPlot.png", format=PngImage())

elif method == 'vtk':
    #### original vtk code

    import vtk

    if len(x) != len(y) != len(dx) != len(dy):
        raise ValueError, "x, y, dx and dy vectors must be of equal length"

    numPoints = len(x)

    # construct the points data
    points = vtk.vtkPoints()
    points.SetNumberOfPoints(numPoints)
    for i in range(numPoints):
        points.InsertPoint(i, x[i], y[i], 0.0)

    # make the vectors
    vectors = vtk.vtkFloatArray()
    vectors.SetNumberOfComponents(3)
    vectors.SetNumberOfTuples(numPoints)
    vectors.SetName("vectors")
    for i in range(numPoints):
        vectors.InsertTuple3(i, dx[i], dy[i], 0.0)

    # construct the grid
    grid = vtk.vtkUnstructuredGrid()
    grid.SetPoints(points)
    grid.GetPointData().AddArray(vectors)
    grid.GetPointData().SetActiveVectors("vectors")

    # make the arrow source
    arrow = vtk.vtkArrowSource()

    # make the glyph
    glyph = vtk.vtkGlyph2D()
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByVector()
    glyph.SetColorModeToColorByVector()
    glyph.SetScaleFactor(0.5)
    glyph.SetSource(arrow.GetOutput())
    glyph.SetInput(grid)
    glyph.ClampingOff()

    # set up a stripper for faster rendering
    stripper = vtk.vtkStripper()
    stripper.SetInput(glyph.GetOutput())

    # get the maximum norm of the data
    maxNorm = grid.GetPointData().GetVectors().GetMaxNorm()

    # now set up the mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(stripper.GetOutput())
    mapper.SetScalarRange(0, maxNorm) 

    # set up the actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # set up the renderer stuff
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(640,480)
    renWin.AddRenderer(ren)
    ren.SetBackground(1,1,1)

    ren.AddActor(actor)

    # set up some text properties
    font_size = 14
    textProp = vtk.vtkTextProperty()
    textProp.SetFontSize(font_size)
    textProp.SetFontFamilyToArial()
    textProp.BoldOff()
    textProp.ItalicOff()
    textProp.ShadowOff()
    textProp.SetColor(0,0,0)

    # add a title
    titleMapper = vtk.vtkTextMapper()
    title = 'Example 2D arrow/quiver/vector field plot'
    titleMapper.SetInput(title)

    titleProp = titleMapper.GetTextProperty()
    titleProp.ShallowCopy(textProp)
    titleProp.SetJustificationToCentered()
    titleProp.SetVerticalJustificationToTop()
    titleProp.SetFontSize(18)

    # set up the text actor
    titleActor = vtk.vtkTextActor()
    titleActor.SetMapper(titleMapper)
    titleActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
    titleActor.GetPositionCoordinate().SetValue(0.5, 0.95)

    ren.AddActor(titleActor)

    # set up some axes
    axes = vtk.vtkCubeAxesActor2D()
    #axes.SetInput(grid)
    axes.SetCamera(ren.GetActiveCamera())
    axes.SetFlyModeToOuterEdges()
    axes.SetBounds(min(x), max(x)+maxNorm, min(y), max(y)+maxNorm, 0, 0)
    axes.SetXLabel("x")
    axes.SetYLabel("y")
    axes.SetZLabel("")
    axes.YAxisVisibilityOff()  # but this is the z axis!!

    axesProp = axes.GetProperty()
    axesProp.SetColor(0,0,0)

    axesTitleProp = axes.GetAxisTitleTextProperty()
    axesTitleProp.ShallowCopy(textProp)

    axesLabelProp = axes.GetAxisLabelTextProperty()
    axesLabelProp.ShallowCopy(textProp)
    axesLabelProp.SetFontSize(8)

    ren.AddActor(axes)

    ren.ResetCamera()

    # set up the interactive renderer and render the scene
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    renWin.Render()
    iren.Start()

    # convert the render window to an image
    win2img = vtk.vtkWindowToImageFilter()
    win2img.SetInput(renWin)

    # save the image to file
    outWriter = vtk.vtkPNGWriter()
    outWriter.SetInput(win2img.GetOutput())
    outWriter.SetFileName("arrowPlot.png")
    outWriter.Write()

elif method == 'plplot':
    #### original plplot code

    print "Sorry, the plplot interface hasn't been written yet."
else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:

