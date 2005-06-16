# $Id$

"""
Example of plotting a 3D vector field with pyvisi 
"""

# what plotting method are we using?
method = 'povray'

# set up some data to plot
from Numeric import *

dim = 10

# initialise the positions of the vectors
x = zeros((dim,dim), typecode=Float)
y = zeros((dim,dim), typecode=Float)
z = zeros((dim,dim), typecode=Float)

# initialise the vector displacements
# (I may need to rethink how this works in the interface)
dx = zeros((dim,dim), typecode=Float)
dy = zeros((dim,dim), typecode=Float)
dz = zeros((dim,dim), typecode=Float)

# set the positions randomly, and set the displacements to some smaller
# random number but of mean zero instead of distributed between 0 and 1
import random
random.seed()
for i in range(dim):
    for j in range(dim):
        x[i,j] = random.random()
        y[i,j] = random.random()
        z[i,j] = random.random()
        dx[i,j] = (random.random()-0.5)/5.0
        dy[i,j] = (random.random()-0.5)/5.0
        dz[i,j] = (random.random()-0.5)/5.0

# plot it using one of the three methods
if method == 'pyvisi':

    # example code for how a user would write a script in pyvisi
    from pyvisi import *          # base level visualisation stuff
    # import the objects to render the scene using the specific renderer
    from pyvisi.renderers.gnuplot import *   # gnuplot
    #from pyvisi.renderers.vtk import *       # vtk
    #from pyvisi.renderers.povray import *    # povray
    
    # define the scene object
    # a Scene is a container for all of the kinds of things you want to put 
    # into your plot for instance, images, meshes, arrow/vector/quiver plots, 
    # contour plots, spheres etc.
    scene = Scene()
    
    # create a ArrowPlot3D object
    plot = ArrowPlot3D(scene)
    
    # add some helpful info to the plot
    plot.title = 'Example 3D arrow/quiver/vector field plot'
    plot.xlabel = 'x'
    plot.ylabel = 'y'
    plot.ylabel = 'z'

    # assign some data to the plot
    plot.setData(x, y, z, dx, dy, dz)

    # render the scene to screen
    scene.render(pause=True, interactive=True)

    # save the scene out to file
    plot.setData(x, y, z, dx, dy, dz) # have to do this because we've already
                               # render()ed the scene.  This requirement
                               # will be removed in the future
    scene.save(fname="arrowPlot3D.png", format=PngImage())

elif method == 'vtk':
    #### original vtk code

    import vtk

    # loading a vtk file as input
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName("vel-0500.vtk")
    reader.Update()

    grid = reader.GetOutput()

    # grab the model centre and bounds
    centre = grid.GetCenter()
    bounds = grid.GetBounds()

    # grab the norm of the vectors
    norm = vtk.vtkVectorNorm()
    norm.SetInput(grid)

    maxNorm = grid.GetPointData().GetVectors().GetMaxNorm()

    # to make arrow glyphs need an arrow source
    arrow = vtk.vtkArrowSource()
    
    # the arrows are 3D glyphs so set that up now
    glyph = vtk.vtkGlyph3D()
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByScalar()
    glyph.SetColorModeToColorByScalar()
    glyph.SetVectorModeToUseVector()
    glyph.SetScaleFactor(0.1/maxNorm)
    glyph.SetInput(norm.GetOutput())
    glyph.SetSource(arrow.GetOutput())
    glyph.ClampingOff()

    # set up a stripper to speed up rendening
    stripper = vtk.vtkStripper()
    stripper.SetInput(glyph.GetOutput())
    
    # make a lookup table for the colour map and invert it (colours look
    # better when it's inverted)
    lut = vtk.vtkLookupTable()
    refLut = vtk.vtkLookupTable()
    lut.Build()
    refLut.Build()
    for j in range(256):
        lut.SetTableValue(j, refLut.GetTableValue(255-j))
    
    # set up the mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(stripper.GetOutput())
    mapper.SetScalarRange(0,maxNorm)
    mapper.SetLookupTable(lut)
    
    # set up the actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
   
    # set up the text properties for nice text
    font_size = 20
    textProp = vtk.vtkTextProperty()
    textProp.SetFontSize(font_size)
    textProp.SetFontFamilyToArial()
    textProp.BoldOff()
    textProp.ItalicOff()
    textProp.ShadowOff()
    textProp.SetColor(0.0, 0.0, 0.0)
 
    # make a title
    title = vtk.vtkTextMapper()
    title.SetInput("Example 3D arrow/quiver/vector field plot")

    # make the title text use the text properties
    titleProp = title.GetTextProperty()
    titleProp.ShallowCopy(textProp)
    titleProp.SetJustificationToCentered()
    titleProp.SetVerticalJustificationToTop()
    titleProp.BoldOn()

    # make the actor for the title
    titleActor = vtk.vtkTextActor()
    titleActor.SetMapper(title)
    titleActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
    titleActor.GetPositionCoordinate().SetValue(0.5, 0.95)

    # put an outline around the data
    outline = vtk.vtkOutlineSource()
    outline.SetBounds(bounds)

    # make its mapper
    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInput(outline.GetOutput())

    # make its actor
    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(0,0,0)

    # set up the renderer and render window
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    
    renWin.SetSize(800,600)
    renWin.AddRenderer(ren)
    ren.SetBackground(1,1,1)
    
    # add the relevant actors
    ren.AddActor(actor)
    ren.AddActor(titleActor)
    ren.AddActor(outlineActor)
   
    cam = ren.GetActiveCamera()
    #cam.Azimuth(0)
    #cam.Elevation(-90)
    cam.Zoom(1.2)
    ren.SetActiveCamera(cam)
    ren.ResetCameraClippingRange()

    # add some axes
    axes = vtk.vtkCubeAxesActor2D()
    axes.SetInput(grid)
    axes.SetCamera(ren.GetActiveCamera())
    axes.SetLabelFormat("%6.4g")
    axes.SetFlyModeToOuterEdges()
    axes.SetFontFactor(0.8)
    axes.SetAxisTitleTextProperty(textProp)
    axes.SetAxisLabelTextProperty(textProp)
    axes.SetXLabel("x")
    axes.SetYLabel("y")
    axes.SetZLabel("z")
    axes.SetNumberOfLabels(5)
    axes.GetProperty().SetColor(0,0,0)
    ren.AddProp(axes)

    # set up stuff for interactive viewing
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    iren.Initialize()
    renWin.Render()
    iren.Start()

    # the WindowToImageFilter is what one uses to save the window to an 
    # image file
    win2img = vtk.vtkWindowToImageFilter()
    win2img.SetInput(renWin)
    
    # set up the PNMWriter as we're saving to png
    writer = vtk.vtkPNGWriter()
    writer.SetFileName("arrowPlot3D.png")
    writer.SetInput(win2img.GetOutput())
    writer.Write()

elif method == 'povray':
    #### original povray code

    import vtk
    import os, sys, re, math
    from Numeric import *
    
    # read in the file
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName("vel-0500.vtk")
    reader.Update()
    
    # get the grid
    grid = reader.GetOutput()
    
    # grab the model centre and bounds
    centre = grid.GetCenter()
    bounds = grid.GetBounds()
    
    # try and extract the vector norm
    norm = vtk.vtkVectorNorm()
    norm.SetInput(grid)
    
    maxNorm = grid.GetPointData().GetVectors().GetMaxNorm()
    
    ### extract the relevant grid data
    
    # the points
    points = grid.GetPoints()
    numPoints = points.GetNumberOfPoints()
    x = zeros(numPoints, typecode=Float)
    y = zeros(numPoints, typecode=Float)
    z = zeros(numPoints, typecode=Float)
    for i in range(numPoints):
        x[i], y[i], z[i] = points.GetPoint(i)
    
    # the data at the points
    data = grid.GetPointData().GetVectors()
    vx = zeros(numPoints, typecode=Float)
    vy = zeros(numPoints, typecode=Float)
    vz = zeros(numPoints, typecode=Float)
    vNorm = zeros(numPoints, typecode=Float)
    for i in range(numPoints):
        vx[i], vy[i], vz[i] = data.GetTuple3(i)
        vNorm[i] = math.sqrt(vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i])
    
    # make a lookup table for the colour map and invert it (colours look
    # better when it's inverted)
    lut = vtk.vtkLookupTable()
    refLut = vtk.vtkLookupTable()
    lut.Build()
    refLut.Build()
    for j in range(256):
        lut.SetTableValue(j, refLut.GetTableValue(255-j))
    
    # get the colours
    r = zeros(numPoints, typecode=Float)
    g = zeros(numPoints, typecode=Float)
    b = zeros(numPoints, typecode=Float)
    for i in range(numPoints):
        r[i], g[i], b[i] = lut.GetColor(vNorm[i]/maxNorm)
    
    ### generate the pov file
    
    pov = open("arrowPlot3D.pov", "w")
    
    pov.write("#include \"colors.inc\"\n")
    pov.write("#include \"shapes.inc\"\n")
    pov.write("#include \"textures.inc\"\n")
    
    pov.write("camera {\n")
    pov.write("  location <%f, %f, -2.5>\n" % (centre[0], centre[1]))
    pov.write("  look_at <%f, %f, -%f>\n" % (centre[0], centre[1], centre[2]))
    pov.write("}\n")
    
    pov.write("light_source {\n")
    pov.write("  <0, 0, -3>\n")
    pov.write("  colour White\n")
    pov.write("}\n")
    
    pov.write("#declare Arrow = union {\n")
    pov.write("  cone {\n")
    pov.write("    <0, 0, 0>, 0.3\n")
    pov.write("    <1, 0, 0>, 0.0\n")
    pov.write("  }\n")
        
    pov.write("  cylinder {\n")
    pov.write("    <-1, 0, 0>\n")
    pov.write("    <0, 0, 0>,\n")
    pov.write("    0.15\n")
    pov.write("  }\n")
    pov.write("}\n")
    
    for i in range(numPoints):
        pov.write("object {\n")
        scale = 0.05*vNorm[i]/maxNorm
        if scale < 1e-8:
            scale = 1e-7
        pov.write("  Arrow scale %g " % scale)
        pov.write("rotate <%f, %f, %f> " % (vx[i], vy[i], vz[i]))
        pov.write("translate <%f, %f, -%f> " % (x[i], y[i], z[i]))
        pov.write("pigment { colour <%f, %f, %f> }\n" % (r[i], g[i], b[i]))
        pov.write("}\n")
    
    pov.close()
    
    ### generate the ini file
    
    # open the ini file to write to
    ini = open("arrowPlot3D.ini", "w")
    
    # the output resolution
    ini.write("Width=640\n")
    ini.write("Height=480\n")
    
    # anti-aliasing settings
    ini.write("Antialias=on\n")
    
    # generate png files
    ini.write("Output_File_Type=N\n")
    
    # the name of the input pov file
    ini.write("Input_File_Name=arrowPlot3D.pov\n")
    
    # pause when done
    ini.write("Pause_When_Done=on\n")
    
    # close the file
    ini.close()
    
    # run povray on the file
    result = os.system("povray arrowPlot3D.ini")
    if result != 0:
        raise SystemError, "Povray execution failed"
    else:
        # clean up a bit
        os.unlink("arrowPlot3D.pov")
        os.unlink("arrowPlot3D.ini")
 
else:
    print "Eeek!  What plotting method am I supposed to use???"

# vim: expandtab shiftwidth=4:

