# Copyright (C) 2004-2005 Paul Cochrane
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

## @file plot.py

"""
Class and functions associated with a pyvisi Plot objects
"""

# generic imports
from pyvisi.renderers.vtk.common import debugMsg
import Numeric
import os

# module specific imports
from pyvisi.renderers.vtk.item import Item

__revision__ = '$Revision$'

class Plot(Item):
    """
    Abstract plot class
    """
    def __init__(self, scene):
        """
        Initialisation of the abstract Plot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        debugMsg(" Called Plot.__init__()")
        Item.__init__(self)

        self.renderer = scene.renderer

        # defaults for plot label-type stuff
        self.title = None
        
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        # list of objects registered with this plot object
        self.objectList = []

    def setData(self, *dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in Plot()")

        if dataList is None:
            raise ValueError, "You must specify a data list"
        
        return

    def setTitle(self, title):
        """
        Set the plot title

        @param title: the string holding the title to the plot
        @type title: string
        """
        debugMsg("Called setTitle() in Plot()")

        self.title = title

        return

    def setXLabel(self, label):
        """
        Set the label of the x-axis

        @param label: the string holding the label of the x-axis
        @type label: string
        """
        debugMsg("Called setXLabel() in Plot()")

        self.xlabel = label

        return

    def setYLabel(self, label):
        """
        Set the label of the y-axis

        @param label: the string holding the label of the y-axis
        @type label: string
        """
        debugMsg("Called setYLabel() in Plot()")

        self.ylabel = label

        return

    def setZLabel(self, label):
        """
        Set the label of the z-axis

        @param label: the string holding the label of the z-axis
        @type label: string
        """
        debugMsg("Called setZLabel() in Plot()")

        self.zlabel = label

        return

    def setLabel(self, axis, label):
        """
        Set the label of a given axis

        @param axis: string (Axis object maybe??) of the axis (e.g. x, y, z)
        @type axis: string or Axis object

        @param label: string of the label to set for the axis
        @type label: string
        """
        debugMsg("Called setLabel() in Plot()")

        # string-wise implementation (really budget implementation too)
        if axis == 'x' or axis == 'X':
            self.xlabel = label
        elif axis == 'y' or axis == 'Y':
            self.ylabel = label
        elif axis == 'z' or axis == 'Z':
            self.zlabel = label
        else:
            raise ValueError, "axis must be x or y or z"

        return

    def _register(self, object):
        """
        Register the given object with the plot object

        This is useful for keeping track of the objects being used to clip
        the current plot object, and for inserting the appropriate code.
        """
        debugMsg("Called Plot._register()")
        self.objectList.append(object)

        return

    def render(self):
        """
        Render the Plot object
        """
        debugMsg("Called Plot.render()")

        return

class ArrowPlot(Plot):
    """
    Arrow field plot
    """
    def __init__(self, scene):
        """
        Initialisation of the ArrowPlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        debugMsg("Called ArrowPlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer

        self.renderer.runString("# ArrowPlot.__init__()")

        # add the plot to the scene
        scene.add(self)

    def setData(self, *dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in ArrowPlot()")

        # do some sanity checking on the data
        if len(dataList) != 4:
            raise ValueError, \
                    "Must have four vectors as input: x, y, dx, dy"

        for i in range(len(dataList)):
            if len(dataList[i].shape) != len(dataList[0].shape):
                raise ValueError, "All arrays must be of the same shape"

        for i in range(len(dataList)):
            if len(dataList[i].shape) != 1 and len(dataList[i].shape) != 2:
                errorString = \
                        "Can only handle 1D or 2D arrays: dim=%d" % \
                        len(dataList[i].shape)
                raise ValueError, errorString

        for i in range(len(dataList)):
            if len(dataList[0]) != len(dataList[i]):
                raise ValueError, "Input vectors must all be the same length"

        # if we have 2D arrays as input, we need to flatten them to plot the
        # data properly
        if len(dataList[0].shape) == 1:
            xData = dataList[0]
            yData = dataList[1]
            dxData = dataList[2]
            dyData = dataList[3]
        elif len(dataList[0].shape) == 2:
            xData = dataList[0].flat
            yData = dataList[1].flat
            dxData = dataList[2].flat
            dyData = dataList[3].flat
        else:
            raise ValueError, "Input vectors can only be 1D or 2D"

	# now pass the data to the render dictionary so that the render code
	# knows what it's supposed to plot
        # x data
        self.renderer.renderDict['_x'] = xData
    
        # y data
        self.renderer.renderDict['_y'] = yData
    
        # dx data
        self.renderer.renderDict['_dx'] = dxData
    
        # dy data
        self.renderer.renderDict['_dy'] = dyData
    
        # keep the number of points for future reference
        numPoints = len(xData)

        # construct the points data
        evalString = "_points = vtk.vtkPoints()\n"
        evalString += "_points.SetNumberOfPoints(%d)\n" % numPoints
	evalString += "for _j in range(%d)\n" % numPoints
	evalString += "    _points.InsertPoint(_j, _x[_j], _y[_j], 0.0)\n"
        self.renderer.runString(evalString)

        # construct the vectors
        evalString = "_vectors = vtk.vtkFloatArray()\n"
        evalString += "_vectors.SetNumberOfComponents(3)\n"
        evalString += "_vectors.SetNumberOfTuples(%d)\n" % numPoints
        evalString += "_vectors.SetName(\"vectors\")\n"
	evalString += "for _j in range(%d)\n" % numPoints
	evalString += "    _vectors.InsertTuple3(_j, _dx[_j], _dy[_j], 0.0)\n"
        self.renderer.runString(evalString)

        # construct the grid
        evalString = "_grid = vtk.vtkUnstructuredGrid()\n"
        evalString += "_grid.SetPoints(_points)\n"
        evalString += "_grid.GetPointData().AddArray(_vectors)\n"
        evalString += "_grid.GetPointData().SetActiveVectors(\"vectors\")"
        self.renderer.runString(evalString)


    def render(self):
        """
        Does ArrowPlot specific rendering tasks
        """
        debugMsg("Called render() in ArrowPlot")
        self.renderer.runString("# ArrowPlot.render()")

        # make the arrow source
        self.renderer.runString("_arrow = vtk.vtkArrowSource()")

        # make the glyph
        evalString = "_glyph = vtk.vtkGlyph2D()\n"
        evalString += "_glyph.ScalingOn()\n"
        evalString += "_glyph.SetScaleModeToScaleByVector()\n"
        evalString += "_glyph.SetColorModeToColorByVector()\n"
        evalString += "_glyph.SetScaleFactor(0.5)\n"
        evalString += "_glyph.SetSource(_arrow.GetOutput())\n"
        evalString += "_glyph.SetInput(_grid)\n"
        evalString += "_glyph.ClampingOff()"
        self.renderer.runString(evalString)

        # set up a stripper for faster rendering
        evalString = "_stripper = vtk.vtkStripper()\n"
        evalString += "_stripper.SetInput(_glyph.GetOutput())"
        self.renderer.runString(evalString)

        # get the maximum norm of the data
        evalString = "_maxNorm = _grid.GetPointData().GetVectors().GetMaxNorm()"
        self.renderer.runString(evalString)

        # set up the mapper
        evalString = "_mapper = vtk.vtkPolyDataMapper()\n"
        evalString += "_mapper.SetInput(_stripper.GetOutput())\n"
        evalString += "_mapper.SetScalarRange(0, _maxNorm)"
        self.renderer.runString(evalString)

        # set up the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.runString(evalString)

        # add the actor
        self.renderer.runString("_renderer.AddActor(_actor)")

        # text properties
        evalString = "_font_size = 14\n"  # this will need to be an option!!
        evalString += "_textProp = vtk.vtkTextProperty()\n"
        evalString += "_textProp.SetFontSize(_font_size)\n"
        evalString += "_textProp.SetFontFamilyToArial()\n"
        evalString += "_textProp.BoldOff()\n"
        evalString += "_textProp.ItalicOff()\n"
        evalString += "_textProp.ShadowOff()\n"
        evalString += "_textProp.SetColor(0,0,0)\n"

        # set the title if set
        if self.title is not None:
            # add a title
            evalString += "_titleMapper = vtk.vtkTextMapper()\n"
            evalString += "_titleMapper.SetInput(\"%s\")\n" % self.title
            
            evalString += "_titleProp = _titleMapper.GetTextProperty()\n"
            evalString += "_titleProp.ShallowCopy(_textProp)\n"
            evalString += "_titleProp.SetJustificationToCentered()\n"
            evalString += "_titleProp.SetVerticalJustificationToTop()\n"
            evalString += "_titleProp.SetFontSize(18)\n"
            
            # set up the text actor
            evalString += "_titleActor = vtk.vtkTextActor()\n"
            evalString += "_titleActor.SetMapper(_titleMapper)\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetCoordinateSystemToNormalizedDisplay()\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetValue(0.5, 0.95)\n"

            evalString += "_renderer.AddActor(_titleActor)"
            self.renderer.runString(evalString)

        # set up some axes
        evalString = "_axes = vtk.vtkCubeAxesActor2D()\n"
        evalString += "_axes.SetCamera(_renderer.GetActiveCamera())\n"
        evalString += "_axes.SetFlyModeToOuterEdges()\n"
        evalString += "_axes.SetBounds(min(_x), max(_x)+_maxNorm, "
        evalString += "min(_y), max(_y)+_maxNorm, 0, 0)\n"

        if self.xlabel is None:
            evalString += "_axes.SetXLabel(\"\")\n"
        else:
            evalString += "_axes.SetXLabel(\"%s\")\n" % self.xlabel

        if self.ylabel is None:
            evalString += "_axes.SetYLabel(\"\")\n"
        else:
            evalString += "_axes.SetYLabel(\"%s\")\n" % self.ylabel

        evalString += "_axes.SetZLabel(\"\")\n"
        evalString += "_axes.YAxisVisibilityOff()\n"  # but this is the z axis!!
        
        # set up the axes properties
        evalString += "_axesProp = _axes.GetProperty()\n"
        evalString += "_axesProp.SetColor(0,0,0)\n"

        # set up the axes title properties
        evalString += "_axesTitleProp = _axes.GetAxisTitleTextProperty()\n"
        evalString += "_axesTitleProp.ShallowCopy(_textProp)\n"
        
        # set up the axes label properties
        evalString += "_axesLabelProp = _axes.GetAxisLabelTextProperty()\n"
        evalString += "_axesLabelProp.ShallowCopy(_textProp)\n"
        evalString += "_axesLabelProp.SetFontSize(8)\n"
        self.renderer.runString(evalString)

        # add the axes to the renderer
        self.renderer.runString("_renderer.AddActor(_axes)")

        # reset the camera, will make things look nicer
        ### is this the right place to put this???
        self.renderer.runString("_renderer.ResetCamera()")
        
        ### this should be somewhere else too...
        self.renderer.runString("_renderer.SetBackground(1,1,1)")

        return

class ArrowPlot3D(Plot):
    """
    Arrow field plot in three dimensions
    """
    def __init__(self, scene):
        """
        Initialisation of the ArrowPlot3D class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        debugMsg("Called ArrowPlot3D.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer

        self.renderer.runString("# ArrowPlot3D.__init__()")

        # default values for fname and format
        self.fname = None
        self.format = None

        # add the plot to the scene
        scene.add(self)

    #def setData(self, fname=None, format=None, *dataList):
    def setData(self, *dataList, **options):
        """
        Set data to the plot

        @param fname: Filename of the input vtk file
        @type fname: string

        @param format: Format of the input vtk file ('vtk' or 'vtk-xml')
        @type format: string

        @param dataList: List of data to set to the plot
        @type dataList: tuple

        @param options: Dictionary of extra options
        @type options: dict
        """
        debugMsg("Called setData() in ArrowPlot3D()")
        self.renderer.runString("# ArrowPlot3D.setData()")

        # process the options, if any
        ## fname
        if options.has_key('fname'):
            fname = options['fname']
        else:
            fname = None
        ## format
        if options.has_key('format'):
            format = options['format']
        else:
            format = None

        # we want to pass this info around
        self.fname = fname
        self.format = format

        # do some sanity checking on the inputs
        if fname is None and format is not None:
            raise ValueError, "Format specified, but no input filename"
        elif fname is not None and format is None:
            raise ValueError, "Filename specified, but no format"
        elif (fname is not None or format is not None) and len(dataList) != 0:
            raise ValueError, \
                "Cannot specify a data list and an input file simultaneously"

        # ok, if we have a data list and no args, use the data list
        if len(dataList) != 0 and fname is None and format is None:
            # do some sanity checking on the data
            if len(dataList) != 6:
                errorStr = "Must have six vectors as input: x, y, z, "
                errorStr += "dx, dy, dz, found: %d" % len(dataList)
                raise ValueError, errorStr
                        
    
            for i in range(len(dataList)):
                if len(dataList[i].shape) != len(dataList[0].shape):
                    raise ValueError, "All arrays must be of the same shape"
    
            for i in range(len(dataList)):
                if len(dataList[i].shape) != 1 and len(dataList[i].shape) != 2:
                    errorString = \
                            "Can only handle 1D or 2D arrays: dim=%d" % \
                            len(dataList[i].shape)
                    raise ValueError, errorString
    
            for i in range(len(dataList)):
                if len(dataList[0]) != len(dataList[i]):
                    raise ValueError, \
                            "Input vectors must all be the same length"
    
            # if we have 2D arrays as input, we need to flatten them to plot the
            # data properly
            if len(dataList[0].shape) == 1:
                xData = dataList[0]
                yData = dataList[1]
                zData = dataList[2]
                dxData = dataList[3]
                dyData = dataList[4]
                dzData = dataList[5]
            elif len(dataList[0].shape) == 2:
                xData = dataList[0].flat
                yData = dataList[1].flat
                zData = dataList[2].flat
                dxData = dataList[3].flat
                dyData = dataList[4].flat
                dzData = dataList[5].flat
            else:
                raise ValueError, "Input vectors can only be 1D or 2D"
    
	    # now pass the data to the render dictionary so that the render
	    # code knows what it's supposed to plot

            # x data
	    self.renderer.renderDict['_x'] = xData
    
            # y data
	    self.renderer.renderDict['_y'] = yData
    
            # z data
	    self.renderer.renderDict['_z'] = zData
    
            # dx data
	    self.renderer.renderDict['_dx'] = dxData
    
            # dy data
	    self.renderer.renderDict['_dy'] = dyData
    
            # dz data
	    self.renderer.renderDict['_dz'] = dzData
    
            # keep the number of points for future reference
            numPoints = len(xData)
    
            # construct the points data
            evalString = "_points = vtk.vtkPoints()\n"
            evalString += "_points.SetNumberOfPoints(%d)\n" % numPoints
	    evalString += "for _j in range(%d):\n" % numPoints
	    evalString += \
		    "    _points.InsertPoint(_j, _x[_j], _y[_j], _z[_j])\n"
            self.renderer.runString(evalString)
    
            # construct the vectors
            evalString = "_vectors = vtk.vtkFloatArray()\n"
            evalString += "_vectors.SetNumberOfComponents(3)\n"
            evalString += "_vectors.SetNumberOfTuples(%d)\n" % numPoints
            evalString += "_vectors.SetName(\"vectors\")\n"
	    evalString += "for _j in range(%d):\n" % numPoints
	    evalString += \
		    "    _vectors.InsertTuple3(_j, _dx[_j], _dy[_j], _dz[_j])\n"
            self.renderer.runString(evalString)
    
            # construct the grid
            evalString = "_grid = vtk.vtkUnstructuredGrid()\n"
            evalString += "_grid.SetPoints(_points)\n"
            evalString += "_grid.GetPointData().AddArray(_vectors)\n"
            evalString += "_grid.GetPointData().SetActiveVectors(\"vectors\")"
            self.renderer.runString(evalString)

        elif len(dataList) == 0 and fname is not None and format is not None:
            # well, lets process the vtk file then

            # had best make sure it exists
            if not os.path.exists(fname):
                raise SystemError, "File: %s not found" % fname
            
            if format == 'vtk':
                # read old-style vtk files
                evalString = "_reader = vtk.vtkUnstructuredGridReader()\n"
            elif format == 'vtk-xml':
                # read vtk xml files
                evalString = "_reader = vtk.vtkXMLUnstructuredGridReader()\n"
            else:
                # barf
                raise ValueError, "Unknown format.  I got %s" % format

            evalString += "_reader.SetFileName(\"%s\")\n" % fname
            evalString += "_reader.Update()"
            self.renderer.runString(evalString)

            # grab the grid
            evalString = "_grid = _reader.GetOutput()"
            self.renderer.runString(evalString)

            # get the norm of the vectors
            evalString = "_norm = vtk.vtkVectorNorm()\n"
            evalString += "_norm.SetInput(_grid)"
            self.renderer.runString(evalString)

        else:
            # barf
            raise ValueError, "Shouldn't have got to here."

    def render(self):
        """
        Does ArrowPlot3D specific rendering tasks
        """
        debugMsg("Called render() in ArrowPlot3D")
        self.renderer.runString("# ArrowPlot3D.render()")

        # make the arrow source
        self.renderer.runString("_arrow = vtk.vtkArrowSource()")

        # get the maximum norm of the data
        evalString = "_maxNorm = _grid.GetPointData().GetVectors().GetMaxNorm()"
        self.renderer.runString(evalString)

        # make the glyph
        evalString = "_glyph = vtk.vtkGlyph3D()\n"
        evalString += "_glyph.ScalingOn()\n"
        evalString += "_glyph.SetScaleModeToScaleByVector()\n"
        evalString += "_glyph.SetColorModeToColorByVector()\n"
        evalString += "_glyph.SetScaleFactor(0.1/_maxNorm)\n"
        # if we have a vtk grid from file, use the norm output of that
        if self.fname is not None and self.format is not None:
            evalString += "_glyph.SetInput(_norm.GetOutput())\n"
        else:
            evalString += "_glyph.SetInput(_grid)\n"
        evalString += "_glyph.SetSource(_arrow.GetOutput())\n"
        evalString += "_glyph.ClampingOff()"
        self.renderer.runString(evalString)

        # set up a stripper for faster rendering
        evalString = "_stripper = vtk.vtkStripper()\n"
        evalString += "_stripper.SetInput(_glyph.GetOutput())"
        self.renderer.runString(evalString)

        # invert the lookup table, so the colours are nicer
        evalString = "_lut = vtk.vtkLookupTable()\n"
        evalString += "_lut.Build()\n"
        evalString += "_refLut = vtk.vtkLookupTable()\n"
        evalString += "_refLut.Build()\n"
        evalString += "for i in range(256):\n"
        evalString += \
                "    _lut.SetTableValue(i, _refLut.GetTableValue(255-i))"
        self.renderer.runString(evalString)

        # set up the mapper
        evalString = "_mapper = vtk.vtkPolyDataMapper()\n"
        evalString += "_mapper.SetInput(_stripper.GetOutput())\n"
        evalString += "_mapper.SetScalarRange(0, _maxNorm)"
        self.renderer.runString(evalString)

        # set up the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.runString(evalString)

        # add the actor
        self.renderer.runString("_renderer.AddActor(_actor)")

        # text properties
        evalString = "_font_size = 14\n"  # this will need to be an option!!
        evalString += "_textProp = vtk.vtkTextProperty()\n"
        evalString += "_textProp.SetFontSize(_font_size)\n"
        evalString += "_textProp.SetFontFamilyToArial()\n"
        evalString += "_textProp.BoldOff()\n"
        evalString += "_textProp.ItalicOff()\n"
        evalString += "_textProp.ShadowOff()\n"
        evalString += "_textProp.SetColor(0,0,0)\n"
        self.renderer.runString(evalString)

        # set the title if set
        if self.title is not None:
            # add a title
            evalString = "_titleMapper = vtk.vtkTextMapper()\n"
            evalString += "_titleMapper.SetInput(\"%s\")\n" % self.title
            
            evalString += "_titleProp = _titleMapper.GetTextProperty()\n"
            evalString += "_titleProp.ShallowCopy(_textProp)\n"
            evalString += "_titleProp.SetJustificationToCentered()\n"
            evalString += "_titleProp.SetVerticalJustificationToTop()\n"
            evalString += "_titleProp.SetFontSize(18)\n"
            
            # set up the text actor
            evalString += "_titleActor = vtk.vtkTextActor()\n"
            evalString += "_titleActor.SetMapper(_titleMapper)\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetCoordinateSystemToNormalizedDisplay()\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetValue(0.5, 0.95)\n"

            evalString += "_renderer.AddActor(_titleActor)"
            self.renderer.runString(evalString)

        # set up some axes
        evalString = "_axes = vtk.vtkCubeAxesActor2D()\n"
        evalString += "_axes.SetCamera(_renderer.GetActiveCamera())\n"
        evalString += "_axes.SetFlyModeToOuterEdges()\n"
        if self.fname is not None and self.format is not None:
            evalString += "_axes.SetInput(_grid)\n"
        else:
            evalString += "_axes.SetBounds(min(_x)-_maxNorm, max(_x)+_maxNorm, "
            evalString += "min(_y)-_maxNorm, max(_y)+_maxNorm, "
            evalString += "min(_z)-_maxNorm, max(_z)+_maxNorm)\n"

        if self.xlabel is None:
            evalString += "_axes.SetXLabel(\"\")\n"
        else:
            evalString += "_axes.SetXLabel(\"%s\")\n" % self.xlabel

        if self.ylabel is None:
            evalString += "_axes.SetYLabel(\"\")\n"
        else:
            evalString += "_axes.SetYLabel(\"%s\")\n" % self.ylabel

        if self.zlabel is None:
            evalString += "_axes.SetZLabel(\"\")\n"
        else:
            evalString += "_axes.SetZLabel(\"%s\")\n" % self.zlabel

        # set up the axes properties
        evalString += "_axesProp = _axes.GetProperty()\n"
        evalString += "_axesProp.SetColor(0,0,0)\n"

        # set up the axes title properties
        evalString += "_axesTitleProp = _axes.GetAxisTitleTextProperty()\n"
        evalString += "_axesTitleProp.ShallowCopy(_textProp)\n"
        
        # set up the axes label properties
        evalString += "_axesLabelProp = _axes.GetAxisLabelTextProperty()\n"
        evalString += "_axesLabelProp.ShallowCopy(_textProp)\n"
        evalString += "_axesLabelProp.SetFontSize(8)\n"
        self.renderer.runString(evalString)

        # add the axes to the renderer
        self.renderer.runString("_renderer.AddActor(_axes)")

        # reset the camera, will make things look nicer
        ### is this the right place to put this???
        self.renderer.runString("_renderer.ResetCamera()")
        
        ### this should be somewhere else too...
        self.renderer.runString("_renderer.SetBackground(1,1,1)")

        return

class BallPlot(Plot):
    """
    Ball plot
    """
    def __init__(self, scene):
        debugMsg("Called BallPlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer

        self.renderer.runString("# BallPlot.__init__()")

        # add the plot to the scene
        scene.add(self)

    def setData(self, points=None, 
            fname=None, format=None,
            radii=None, colors=None, tags=None):
        """
        Set data to the plot
        @param points: the array to use for the points of the sphere
        locations in space
        @type points: float array

        @param fname: the name of the input vtk file
        @type fname: string

        @param format: the format of the input vtk file ('vtk' or 'vtk-xml')
        @type format: string

        @param radii: the name of the scalar array in the vtk unstructured
        grid to use as the radii of the balls
        @type radii: float array

        @param colors: the name of the scalar array in the vtk unstructured
        grid to use as the colour tags of the balls
        @type colors: string

        @param tags: the name of the scalar array in the vtk unstructured
        grid to use as the colour of the tags of the balls
        @type tags: integer array
        """
        debugMsg("Called setData() in BallPlot()")
        self.renderer.runString("# BallPlot.setData()")

        # check that we have enough info to start with
        if points is None and fname is None:
            errorString = "You must supply either appropriate arrays of\n\
                    data or the name of a vtk file for input"
            raise ValueError, errorString

        # need to also check if they're both specified
        if points is not None and fname is not None:
            raise ValueError, \
                    "Sorry, you can't specify both a data list and a filename"

        # now check the bits required if the fname option is set
        if fname is not None:
            if format is None:
                raise ValueError, "You must specify a vtk file format"
            elif radii is None:
                raise ValueError, \
                "You must specify the name of the scalars to use as the radius"
            elif colors is None and tags is None:
                raise ValueError, \
                "You must specify the name of the scalars to use for the colors"

        # now check that the format is logical
        if format is not None and format != "vtk" and format != "vtk-xml":
            errorString = \
                "Unknown format: must be either 'vtk' or 'vtk-xml'\n"
            errorString += "I got: %s" % format
            raise ValueError, errorString

        # for now just hope that if the stuff is specified, that it agrees
        # with what's in the vtk unstructured grid

        if format is not None and (format == "vtk-xml" or format == "vtk"):
            if format == "vtk-xml":
                debugMsg("Using vtk-xml file as input")
                # create the reader of the file
                evalString = "_reader = vtk.vtkXMLUnstructuredGridReader()\n"
                evalString += "_reader.SetFileName(\"%s\")\n" % fname
                evalString += "_reader.Update()"
                self.renderer.runString(evalString)
            elif format == "vtk":
                debugMsg("Using old-style vtk file as input")
                # create the reader of the file
                evalString = "_reader = vtk.vtkUnstructuredGridReader()\n"
                evalString += "_reader.SetFileName(\"%s\")\n" % fname
                evalString += "_reader.Update()"
                self.renderer.runString(evalString)

            # read the output to an unstructured grid
            self.renderer.runString("_grid = _reader.GetOutput()")

            # note that these next few steps are only necessary in vtk 4.2,
            # 4.4 grab the data to use for the radii of the balls
            evalString = \
                    "_radii = _grid.GetPointData().GetScalars(\"%s\")" % \
                    radii
            self.renderer.runString(evalString)
    
            # grab the data to use for colouring the balls
            if colors is None:
                evalString = \
                    "_colours = _grid.GetPointData().GetScalars(\"%s\")" %\
                    tags
            else:
                evalString = \
                    "_colours = _grid.GetPointData().GetScalars(\"%s\")" % \
                    colors
            self.renderer.runString(evalString)
    
            # now work out the number of tags, and their values
            evalString = "_numPoints = _colours.GetNumberOfTuples()\n"
            evalString += "_valueDict = {}\n"
            evalString += "for i in range(_numPoints):\n"
            evalString += "    _colourValue = _colours.GetValue(i)\n"
            evalString += "    _valueDict[_colourValue] = 1\n"
    
            evalString += "_numColours = len(_valueDict.keys())\n"
    
            evalString += "_colourValues = _valueDict.keys()\n"
            evalString += "_colourValues.sort()"
            self.renderer.runString(evalString)
    
            # now count the number of colours, and make an evenly spaced
            # array of points between zero and one, then use these as the
            # scalars to colour by
            evalString = "_scaledColours = vtk.vtkFloatArray()\n"
            evalString += "_scaledColours.SetNumberOfTuples(_numPoints)\n"
            evalString += "_scaledColours.SetNumberOfComponents(1)\n"
            evalString += "_scaledColours.SetName(\"scaledColours\")\n"
            evalString += "for i in range(_numPoints):\n"
            evalString += "    _colourValue = _colours.GetValue(i)\n"
            evalString += "    for j in range(_numColours):\n"
            evalString += "        if _colourValues[j] == _colourValue:\n"
            evalString += "            _scaledColours.InsertTuple1(i,"
            evalString += "float(j)/float(_numColours-1))"
            self.renderer.runString(evalString)
    
            # now set up an array of two components to get the data through
            # the glyph object to the mapper (this is so that colouring and
            # scalaing work properly)
            evalString = "_data = vtk.vtkFloatArray()\n"
            evalString += "_data.SetNumberOfComponents(3)\n"
            evalString += \
                    "_data.SetNumberOfTuples(_radii.GetNumberOfTuples())\n"
            evalString += "_data.CopyComponent(0, _radii, 0)\n"
            evalString += "_data.CopyComponent(1, _colours, 0)\n"
            evalString += "_data.CopyComponent(2, _scaledColours, 0)\n"
            evalString += "_data.SetName(\"data\")"
            self.renderer.runString(evalString)
    
            # add the data array to the grid
            evalString = "_grid.GetPointData().AddArray(_data)\n"
    
            # make the data the active scalars
            evalString += "_grid.GetPointData().SetActiveScalars(\"data\")"
            self.renderer.runString(evalString)

        elif format is None and points is not None:
            debugMsg("Using user-defined point data in BallPlot.setData()")
            ### if we get to here, then we have to construct the points,
            ### the radii and the colours all from scratch, add them to the
            ### grid and get everthing in the same form that we have for the
            ### case where we load a vtk data file

            numPoints = len(points)
            numRadii = len(radii)
            # do some sanity checking on the data
            if numRadii != numPoints:
                raise ValueError, \
                    "The number of points does not equal the number of radii"

            ### construct the grid from the point data
            # make the points
            evalString = "_points = vtk.vtkPoints()\n"
            evalString += "_points.SetNumberOfPoints(%d)\n" % numPoints
            for i in range(numPoints):
                point = points[i]
                evalString += "_points.InsertPoint(%d, %f, %f, %f)\n" % \
                        (i, point[0], point[1], point[2])
            self.renderer.runString(evalString)

            # make the radii
            evalString = "_radii = vtk.vtkFloatArray()\n"
            evalString += "_radii.SetNumberOfComponents(1)\n"
            evalString += "_radii.SetNumberOfValues(%d)\n" % numPoints
            for i in range(numPoints):
                evalString += "_radii.InsertValue(%d, %f)\n" % (i, radii[i])
            self.renderer.runString(evalString)

            # make the colours
            if colors is None:
                # ok then, since we have no info, make them related to the
                # radii
                pass

            # what if we have a tags argument as well, and use that for the
            # colours if the colours array doesn't exists (which would be
            # more complicated for the user to set up, but can have the
            # functionality if someone wants to use it)

            if tags is None:
                debugMsg("Autogenerating tags in BallPlot.setData()")
                # relate the tags to the radii
                # need to find the number of different radii
                radiiDict = {}
                for i in range(numPoints):
                    radiiDict[str(radii[i])] = 1
                numRadii = len(radiiDict.keys())
                radiiKeys = radiiDict.keys()
                # now just make a list of evenly spaced tags up to numRadii
                tagValues = range(numRadii)
                numTags = numRadii

                tags = Numeric.zeros(numPoints, typecode=Numeric.Int)
                for i in range(numPoints):
                    for j in range(numTags):
                        if radiiKeys[j] == str(radii[i]):
                            tags[i] = tagValues[j]

            elif tags is not None:
                msg = "Using tag data for colour information in "
                msg += "BallPlot.setData()"
                debugMsg(msg)

                # check that the number of tags is correct
                if len(tags) != numPoints:
                    errorString = "The number of tags needs to be the"
                    errorString += "same as the number of points"
                    raise ValueError, errorString

                # need to find out the number of different tags
                valueDict = {}
                for i in range(numPoints):
                    valueDict[tags[i]] = 1
                numTags = len(valueDict.keys())
                tagValues = valueDict.keys()
                tagValues.sort()

            # give the tag data to vtk
            evalString = "_tags = vtk.vtkFloatArray()\n"
            evalString += "_tags.SetNumberOfValues(%d)\n" % numPoints
            evalString += "_tags.SetNumberOfComponents(1)\n"
            evalString += "_tags.SetName(\"tags\")\n"
            for i in range(numPoints):
                evalString += "_tags.InsertValue(%d, %d)\n" % \
                        (i, tags[i])
            self.renderer.runString(evalString)

            # now scale the tags
            scaledTags = Numeric.zeros(numPoints, typecode=Numeric.Float)
            if numTags == 1:
                pass
            else:
                for i in range(numPoints):
                    for j in range(numTags):
                        if tagValues[j] == tags[i]:
                            scaledTags[i] = float(j)/float(numTags-1)

            # now give vtk the scaled tag data
            evalString = "_scaledTags = vtk.vtkFloatArray()\n"
            evalString += "_scaledTags.SetNumberOfValues(%d)\n" % numPoints
            evalString += "_scaledTags.SetNumberOfComponents(1)\n"
            evalString += "_scaledTags.SetName(\"scaledTags\")\n"
            for i in range(numPoints):
                evalString += "_scaledTags.InsertValue(%d, %f)\n" % \
                        (i, scaledTags[i])
            self.renderer.runString(evalString)

            # now construct the data array
            ### this is a vtk 4.2, 4.4 specific thing.  vtk 4.5 and above
            ### have a better way to do it, but this is here for backwards 
            ### compatibility
            evalString = "_data = vtk.vtkFloatArray()\n"
            evalString += "_data.SetNumberOfComponents(3)\n"
            evalString += \
                    "_data.SetNumberOfTuples(_radii.GetNumberOfTuples())\n"
            evalString += "_data.CopyComponent(0, _radii, 0)\n"
            evalString += "_data.CopyComponent(1, _tags, 0)\n"
            evalString += "_data.CopyComponent(2, _scaledTags, 0)\n"
            evalString += "_data.SetName(\"data\")\n"
            self.renderer.runString(evalString)

            # now construct the grid
            evalString = "_grid = vtk.vtkUnstructuredGrid()\n"
            evalString += "_grid.SetPoints(_points)\n"

            # add the data array to the grid
            evalString += "_grid.GetPointData().AddArray(_data)\n"

            # make the data the active scalars
            evalString += "_grid.GetPointData().SetActiveScalars(\"data\")\n"

            self.renderer.runString(evalString)
        else:
            # barf
            raise ValueError, \
                    "Cannot construct BallPlot with the given input.  Exiting."

        return

    def render(self):
        """
        Does BallPlot specific rendering tasks
        """
        debugMsg("Called render() in BallPlot")
        self.renderer.runString("# BallPlot.render()")

        # to make sphere glyphs need a sphere source
        evalString = "_sphere = vtk.vtkSphereSource()\n"
        evalString += "_sphere.SetRadius(1.0)\n"
        evalString += "_sphere.SetThetaResolution(5)\n"
        evalString += "_sphere.SetPhiResolution(5)"
        self.renderer.runString(evalString)

        # the spheres are 3D glyphs so set that up
        evalString = "_glyph = vtk.vtkGlyph3D()\n"
        evalString += "_glyph.ScalingOn()\n"
        evalString += "_glyph.SetScaleModeToScaleByScalar()\n"
        evalString += "_glyph.SetColorModeToColorByScalar()\n"
        evalString += "_glyph.SetScaleFactor(1.0)\n"
        evalString += "_glyph.SetInput(_grid)\n"
        evalString += "_glyph.SetSource(_sphere.GetOutput())\n"
        evalString += "_glyph.ClampingOff()"
        self.renderer.runString(evalString)

        # set up a stripper (this will speed up rendering)
        evalString = "_stripper = vtk.vtkStripper()\n"
        evalString += "_stripper.SetInput(_glyph.GetOutput())\n"

        # denote the stripper as being before the mapper by default, and let
        # subsequent objects redefine this if necessary
        evalString += "_preMapper = _stripper"
        self.renderer.runString(evalString)

        # if any clip objects etc are registered, then get them to render
        # themselves here
        for obj in self.objectList:
            obj.render()

        # set up the mapper
        evalString = "_mapper = vtk.vtkPolyDataMapper()\n"
        evalString += "_mapper.SetInput(_preMapper.GetOutput())\n"
        evalString += "_mapper.ScalarVisibilityOn()\n"
        # note: this is for vtk 4.2, 4.4 (4.5 and above have a better
        # technique to colour the scalars, but that version isn't yet
        # standard, or in fact released)
        evalString += "_mapper.ColorByArrayComponent(\"data\", 2)\n"
        # should be done in setData()
        evalString += "_mapper.SetScalarRange(0, 1)"
        self.renderer.runString(evalString)

        # set up the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.runString(evalString)

        # add the actor to the scene
        self.renderer.runString("_renderer.AddActor(_actor)")

        # set the title if set
        if self.title is not None:
            # text properties
            evalString = "_font_size = 20\n"  # this will need to be an option!!
            evalString += "_textProp = vtk.vtkTextProperty()\n"
            evalString += "_textProp.SetFontSize(_font_size)\n"
            evalString += "_textProp.SetFontFamilyToArial()\n"
            evalString += "_textProp.BoldOff()\n"
            evalString += "_textProp.ItalicOff()\n"
            evalString += "_textProp.ShadowOff()\n"
            evalString += "_textProp.SetColor(0,0,0)\n"
        
            # add a title
            evalString += "_titleMapper = vtk.vtkTextMapper()\n"
            evalString += "_titleMapper.SetInput(\"%s\")\n" % self.title
            
            evalString += "_titleProp = _titleMapper.GetTextProperty()\n"
            evalString += "_titleProp.ShallowCopy(_textProp)\n"
            evalString += "_titleProp.SetJustificationToCentered()\n"
            evalString += "_titleProp.SetVerticalJustificationToTop()\n"
            evalString += "_titleProp.BoldOn()\n"
            
            # set up the text actor
            evalString += "_titleActor = vtk.vtkTextActor()\n"
            evalString += "_titleActor.SetMapper(_titleMapper)\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetCoordinateSystemToNormalizedDisplay()\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetValue(0.5, 0.95)\n"

            evalString += "_renderer.AddActor(_titleActor)"
            self.renderer.runString(evalString)

        return
        
class ContourPlot(Plot):
    """
    Contour plot
    """
    def __init__(self, scene):
        """
        Initialisation of the ContourPlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        debugMsg("Called ContourPlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer

        # default values for shared info
        self.fname = None
        self.format = None
        self.scalars = None
        self.escriptData = False
        self.otherData = False

        # add the plot to the scene
        scene.add(self)

    #def setData(self, fname=None, format=None, scalars=None, 
            #*dataList, **options):
    def setData(self, *dataList, **options):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple

        @param fname: the name of the input vtk file
        @type fname: string

        @param format: the format of the input vtk file ('vtk' or 'vtk-xml')
        @type format: string

        @param scalars: the scalar data in the vtk file to use
        @param scalars: string
        """
        debugMsg("Called setData() in ContourPlot()")
        self.renderer.runString("# ContourPlot.setData()")

        # get the options, if any
        ## fname
        if options.has_key('fname'):
            fname = options['fname']
        else:
            fname = None
        ## format
        if options.has_key('format'):
            format = options['format']
        else:
            format = None
        ## scalars
        if options.has_key('scalars'):
            scalars = options['scalars']
        else:
            scalars = None

        # we want to pass this info around
        self.fname = fname
        self.format = format
        self.scalars = scalars

        # do some sanity checking on the input args
        if len(dataList) == 0 and fname is None:
            raise ValueError, \
                    "You must specify a data list or an input filename"

        if len(dataList) != 0 and fname is not None:
            raise ValueError, \
                    "You cannot specify a data list as well as an input file"

        if fname is not None and scalars is None:
            print fname
            raise ValueError, "You must specify which scalars to use"

        if fname is not None and format is None:
            print fname
            raise ValueError, "You must specify an input file format"

        # if have just a data list, check the objects passed in to see if
        # they are escript data objects or not
        escriptData = False
        otherData = False
        self.escriptData = False
        self.otherData = False
        for obj in dataList:
            try:
                obj.convertToNumArray()
                # ok, we've got escript data, set the flag
                escriptData = True
                self.escriptData = True
            except AttributeError:
                otherData = True
                self.otherData = True

        # if we have both escript data and other data, barf as can't handle
        # that yet
        if escriptData and otherData:
            raise TypeError, \
                    "Sorry, can't handle both escript and other data yet"
        
        elif escriptData and not otherData:
            # do we have access to escript??
            try:
                # escript objects should be able to be converted to numarrays
                # so use this as our test if escript is available
                dataList[0].convertToNumArray()
                debugMsg("Using escript")
            except AttributeError:
                raise ImportError, "Unable to use escript"

        else:
            # well, just try and handle the data normally
            pass

        # now generate the code for the case when we have escript data
        # just passed into setData()
        if escriptData:
            # now need to check if have Finley or Bruce mesh
            # note that Bruce isn't actually implemented yet
            # do I need to worry about this in vtk???  I'll be just using
            # an unstructured grid anyway...
            
            ##!!!!  need to check for rank of data so know if it is 
            ##!!!!  scalar or not, if other than scalar have to do
            ##!!!!  something other than am doing here

            # get the relevant bits of data
            if len(dataList) == 1:
                # only one data variable, will need to get the domain from it
                ### the capital letter denotes this is an escript object
                escriptZ = dataList[0]
                escriptX = escriptZ.getDomain().getX()
            elif len(dataList) == 2:
                # first variable should be the domain, the second the data
                escriptX = dataList[0]
                escriptZ = dataList[1]
            else:
                errorString = \
                        "Expecting 1 or 2 elements in data list.  I got: %d" \
                        % len(dataList)
                raise ValueError, errorString

            # convert the data to numarray
            xData = escriptX[0].convertToNumArray()
            yData = escriptX[1].convertToNumArray()
            zData = escriptZ.convertToNumArray()

            # pass the data through to the pyvisi renderer
            ### the x data
            evalString = "_x = array(["
            for i in range(len(xData)-1):
                evalString += "%s, " % xData[i]
            evalString += "%s])" % xData[-1]
            self.renderer.runString(evalString)

            ### the y data
            evalString = "_y = array(["
            for i in range(len(yData)-1):
                evalString += "%s, " % yData[i]
            evalString += "%s])" % yData[-1]
            self.renderer.runString(evalString)

            ### the z data
            evalString = "_z = array(["
            for i in range(len(zData)-1):
                evalString += "%s, " % zData[i]
            evalString += "%s])" % zData[-1]
            self.renderer.runString(evalString)

            # calculate the max and min of the z data
            evalString = "_zMin = min(_z)\n"
            evalString += "_zMax = max(_z)"
            self.renderer.runString(evalString)

            # create the points
            evalString = "_points = vtk.vtkPoints()\n"
            evalString += "_points.SetNumberOfPoints(len(_x))\n"
            evalString += "for i in range(len(_x)):\n"
            evalString += "    _points.InsertPoint(i, _x[i], _y[i], 0)"
            self.renderer.runString(evalString)

            # create the data
            evalString = "_data = vtk.vtkFloatArray()\n"
            evalString += "_data.SetNumberOfComponents(1)\n"
            evalString += "_data.SetNumberOfValues(len(_z))\n"
            evalString += "for i in range(len(_z)):\n"
            evalString += "    _data.InsertValue(i, _z[i])"
            self.renderer.runString(evalString)

            # set up the grid (it's polydata since we're doing a Delaunay2D)
            evalString = "_grid = vtk.vtkPolyData()\n"
            evalString += "_grid.SetPoints(_points)\n"
            evalString += "_grid.GetPointData().SetScalars(_data)"
            self.renderer.runString(evalString)

        elif otherData:
            # in this case, we can only accept data lists of length 1 or 3
            # a length of 2 creates an abiguity
            if len(dataList) == 1:
                # need to autogenerate the x and y data
                zData = dataList[0]
                # check that the zData has the right shape
                if len(zData.shape) != 2:
                    raise ValueError, \
                            "z data array is not of correct shape: %s" % \
                            zData.shape
                # autogen the x and y data
                zShape = zData.shape
                xData = range(1, zShape[0]+1)
                yData = range(1, zShape[1]+1)
                # check was created correctly just in case
                if len(xData) != zShape[0]:
                    raise ValueError, \
                        "Autogenerated xData not equal to first dim of zData"
                if len(yData) != zShape[1]:
                    raise ValueError, \
                        "Autogenerated yData not equal to second dim of zData"

            elif len(dataList) == 2:
                raise ValueError, \
                    "The data list can't be of length 2 for non-escript data"
            elif len(dataList) == 3:
                # now just pass the x, y and z data through to the renderer
                xData = dataList[0]
                yData = dataList[1]
                zData = dataList[2]
            else:
                raise ValueError, \
                    "Expecting a data list length of 1 or 3.  I got: %d" \
                    % len(dataList)

            # check the shapes of the data
            if len(xData.shape) != 1:
                raise ValueError, "x data array is not of correct shape: %s"% \
                        xData.shape

            if len(yData.shape) != 1:
                raise ValueError, "y data array is not of correct shape: %s"% \
                        yData.shape

            if len(zData.shape) != 2:
                raise ValueError, "z data array is not of correct shape: %s"% \
                        zData.shape

            # stringify the data to then pass to the renderer
            ### x data
            evalString = "_x = array(["
            for i in range(len(xData)-1):
                evalString += "%s, " % xData[i]
            evalString += "%s])" % xData[-1]
            self.renderer.runString(evalString)

            ### y data
            evalString = "_y = array(["
            for i in range(len(yData)-1):
                evalString += "%s, " % yData[i]
            evalString += "%s])" % yData[-1]
            self.renderer.runString(evalString)

            ### z data
            evalString = "_z = array(["
            for i in range(len(xData)):
                evalString += "["
                for j in range(len(yData)-1):
                    evalString += "%s, " % zData[i, j]
                evalString += "%s],\n" % zData[i, -1]
            evalString += "])"
            self.renderer.runString(evalString)

            # calculate the min and max
            evalString = "_zMax = max(_z.flat)\n"
            evalString += "_zMin = min(_z.flat)"
            self.renderer.runString(evalString)

            # create the points
            evalString = "_points = vtk.vtkPoints()\n"
            evalString += "_points.SetNumberOfPoints(len(_x)*len(_y))\n"
            evalString += "_count = 0\n"
            evalString += "for i in range(len(_x)):\n"
            evalString += "  for j in range(len(_y)):\n"
            evalString += "    _points.InsertPoint(_count, _x[i], _y[j], 0)\n"
            evalString += "    _count += 1"
            self.renderer.runString(evalString)

            # create the data
            evalString = "_data = vtk.vtkFloatArray()\n"
            evalString += "_data.SetNumberOfComponents(1)\n"
            evalString += "_data.SetNumberOfValues(len(_x)*len(_y))\n"
            evalString += "_count = 0\n"
            evalString += "for i in range(len(_x)):\n"
            evalString += "  for j in range(len(_y)):\n"
            evalString += "    _data.InsertValue(_count, _z[i][j])\n"
            evalString += "    _count += 1"
            self.renderer.runString(evalString)

            # set up the grid (it's polydata since we're doing a Delaunay2D)
            evalString = "_grid = vtk.vtkPolyData()\n"
            evalString += "_grid.SetPoints(_points)\n"
            evalString += "_grid.GetPointData().SetScalars(_data)"
            self.renderer.runString(evalString)

        # run the stuff for when we're reading from file
        if fname is not None:
            # create the reader of the file
            evalString = "_reader = vtk.vtkXMLUnstructuredGridReader()\n"
            evalString += "_reader.SetFileName(\"%s\")\n" % fname
            evalString += "_reader.Update()"
            self.renderer.runString(evalString)
    
            # read the output input an unstructured grid
            evalString = "_grid = _reader.GetOutput()\n"
            evalString += \
                    "_grid.GetPointData().SetActiveScalars(\"%s\")" % scalars
            self.renderer.runString(evalString)
    
            # grab the range of scalars for appropriate scaling of the colourmap
            evalString = \
                "_scalarRange = _grid.GetPointData().GetScalars().GetRange()\n"
            evalString += "_scalarMin = _scalarRange[0]\n"
            evalString += "_scalarMax = _scalarRange[1]\n"
            self.renderer.runString(evalString)

        return

    def render(self):
        """
        Does ContourPlot object specific (pre)rendering stuff
        """
        debugMsg("Called ContourPlot.render()")

        self.renderer.runString("# ContourPlot.render()")

        # set up the lookup table and reverse the order of the colours
        evalString = "_lut = vtk.vtkLookupTable()\n"
        evalString += "_lut.Build()\n"
        evalString += "_refLut = vtk.vtkLookupTable()\n"
        evalString += "_refLut.Build()\n"
        evalString += "for i in range(256):\n"
        evalString += \
                "    _lut.SetTableValue(i, _refLut.GetTableValue(255-i))"
        self.renderer.runString(evalString)

        if self.escriptData or self.otherData:
            # triangulate the data
            evalString = "_delaunay = vtk.vtkDelaunay2D()\n"
            evalString += "_delaunay.SetInput(_grid)\n"
            evalString += "_delaunay.SetTolerance(0.001)"
            self.renderer.runString(evalString)

            # set up the mapper
            evalString = "_mapper = vtk.vtkPolyDataMapper()\n"
            evalString += "_mapper.SetInput(_delaunay.GetOutput())\n"
            evalString += "_mapper.SetLookupTable(_lut)\n"
            # note that zMin and zMax are evaluated in setData()
            evalString += "_mapper.SetScalarRange(_zMin, _zMax)"
            self.renderer.runString(evalString)

        elif self.fname is not None:
            # set up the mapper
            evalString = "_mapper = vtk.vtkDataSetMapper()\n"
            evalString += "_mapper.SetInput(_grid)\n"
            evalString += "_mapper.ScalarVisibilityOn()\n"
            evalString += "_mapper.SetLookupTable(_lut)\n"
            evalString += "_mapper.SetScalarRange(_scalarMin, _scalarMax)"
            self.renderer.runString(evalString)

        # set up the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.runString(evalString)

        # add the actor to the scene
        self.renderer.runString("_renderer.AddActor(_actor)")

        # set up the text
        # properties (I think this should come from the pyvisi Text() object
        # at some stage, but we'll hard code it here...)
        # I'll also need separate properties for axes, titles, labels etc...
        # but keep them all the same just to get this going
        evalString = "_textProp = vtk.vtkTextProperty()\n"
        evalString += "_textProp.SetFontFamilyToArial()\n"
        evalString += "_textProp.BoldOff()\n"
        evalString += "_textProp.ItalicOff()\n"
        evalString += "_textProp.ShadowOff()\n"
        evalString += "_textProp.SetColor(0,0,0)\n"
        self.renderer.runString(evalString)

        # set the title if set
        if self.title is not None:
            evalString = "_title = vtk.vtkTextMapper()\n"
            evalString += "_title.SetInput(\"%s\")\n" % self.title
            # make the title text use the text properties
            evalString += "_titleProp = _title.GetTextProperty()\n"
            evalString += "_titleProp.ShallowCopy(_textProp)\n"
            evalString += "_titleProp.SetJustificationToCentered()\n"
            evalString += "_titleProp.SetVerticalJustificationToTop()\n"
            evalString += "_titleProp.SetFontSize(20)\n"
            evalString += "_titleProp.BoldOn()\n"
            # make the actor for the title
            evalString += "_titleActor = vtk.vtkTextActor()\n"
            evalString += "_titleActor.SetMapper(_title)\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetCoordinateSystemToNormalizedDisplay()\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetValue(0.5,0.95)\n"# this should be user-settable
            # add the actor to the scene
            evalString += "_renderer.AddActor(_titleActor)"
            self.renderer.runString(evalString)

        # add the axes
        evalString = "_axes = vtk.vtkCubeAxesActor2D()\n"
        evalString += "_axes.SetInput(_grid)\n"
        evalString += "_axes.SetCamera(_renderer.GetActiveCamera())\n"
        evalString += "_axes.SetLabelFormat(\"%6.4g\")\n"
        evalString += "_axes.SetFlyModeToOuterEdges()\n"
        evalString += "_axes.SetFontFactor(0.8)\n"
        evalString += "_axes.SetAxisTitleTextProperty(_textProp)\n"
        evalString += "_axes.SetAxisLabelTextProperty(_textProp)\n"
        evalString += "_axes.GetProperty().SetColor(0,0,0)\n"
        # this next line sets the Z axis visibility off!!  Is a bug in vtk
        # 4.2, dunno how am going to handle this if it is fixed in later
        # versions of vtk
        evalString += "_axes.YAxisVisibilityOff()\n"
        evalString += "_axes.SetNumberOfLabels(5)\n"

        # if we have an xlabel set it
        if self.xlabel is not None:
            evalString += "_axes.SetXLabel(\"%s\")\n" % self.xlabel
        else:
            evalString += "_axes.SetXLabel(\"\")\n"

        # if we have a ylabel set it
        if self.ylabel is not None:
            evalString += "_axes.SetYLabel(\"%s\")\n" % self.ylabel
        else:
            evalString += "_axes.SetXLabel(\"\")\n"

        # add the axes to the scene
        evalString += "_renderer.AddProp(_axes)"
        self.renderer.runString(evalString)

        # add a scalar bar (need to make this an option somewhere!!)
        # I also need to add the ability for the user to set the values of
        # the various parameters set below, and some kind of logical
        # defaults similar to or the same as what I have below.
        evalString = "_scalarBar = vtk.vtkScalarBarActor()\n"
        evalString += "_scalarBar.SetLookupTable(_lut)\n"
        evalString += "_scalarBar.SetWidth(0.1)\n"
        evalString += "_scalarBar.SetHeight(0.7)\n"
        evalString += "_scalarBar.SetPosition(0.9, 0.2)\n"

        # set up the label text properties 
        evalString += "_scalarBarTextProp = _scalarBar.GetLabelTextProperty()\n"
        evalString += "_scalarBarTextProp.ShallowCopy(_textProp)\n"
        evalString += "_scalarBarTextProp.SetFontSize(10)\n"
    
        # add the scalar bar to the scene
        evalString += "_renderer.AddActor(_scalarBar)\n"
        self.renderer.runString(evalString)

        return

class EllipsoidPlot(Plot):
    """
    Ellipsoid plot
    """
    def __init__(self, scene):
        """
        Initialisation of the EllipsoidPlot class

        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        debugMsg("Called EllipsoidPlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer
        self.renderer.addToInitStack("# EllipsoidPlot.__init__()")

        # labels and stuff
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None
        
        # default values for fname anf format
        self.fname = None
        self.format = None

        # add the plot to the scene
        scene.add(self)

    def setData(self, *dataList, **options):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple

        @param options: Dictionary of keyword options to the method
        @type options: dict
        """
        debugMsg("Called setData() in EllipsoidPlot()")

        self.renderer.runString("# EllipsoidPlot.setData()")

        # process the options, if any
        ## fname
        if options.has_key('fname'):
            fname = options['fname']
        else:
            fname = None
        ## format
        if options.has_key('format'):
            format = options['format']
        else:
            format = None

        # do a quick sanity check on the inputs
        if fname is None or format is None:
            raise ValueError, "You must supply an input file and its format"

        # we want to pass this info around
        self.fname = fname
        self.format = format

        # check to see if the file exists
        if not os.path.exists(fname):
            raise SystemError, "File %s not found" % fname

        if format == 'vtk':
            # read old-style vtk files
            evalString = "_reader = vtk.vtkUnstructuredGridReader()\n"
        elif format == 'vtk-xml':
            # read vtk xml files
            evalString = "_reader = vtk.vtkXMLUnstructuredGridReader()\n"
        else:
            # barf
            raise ValueError, "Unknown format.  I got %s" % format

        evalString += "_reader.SetFileName(\"%s\")\n" % fname
        evalString += "_reader.Update()"

        self.renderer.runString(evalString)

        # grab the grid of the data
        self.renderer.runString("_grid = _reader.GetOutput()")

        # convert the cell data to point data
        evalString = "_c2p = vtk.vtkCellDataToPointData()\n"
        evalString += "_c2p.SetInput(_grid)"
        self.renderer.runString(evalString)

        # now extract the tensor components
        evalString = "_extract = vtk.vtkExtractTensorComponents()\n"
        evalString += "_extract.SetInput(_c2p.GetOutput())\n"
        evalString += "_extract.SetScalarModeToEffectiveStress()\n"
        evalString += "_extract.ExtractScalarsOn()\n"
        evalString += "_extract.PassTensorsToOutputOn()\n"
        evalString += "_extract.ScalarIsEffectiveStress()\n"

        evalString += "_extractGrid = _extract.GetOutput()\n"
        evalString += "_extractGrid.Update()\n"
        evalString += "_extractScalarRange = "
        evalString += "_extractGrid.GetPointData().GetScalars().GetRange()\n"
        self.renderer.runString(evalString)

        return

    def render(self):
        """
        Does EllipsoidPlot object specific (pre)rendering stuff
        """
        debugMsg("Called EllipsoidPlot.render()")

        self.renderer.runString("# EllipsoidPlot.render()")

        # make a sphere source for the glyphs
        evalString = "_sphere = vtk.vtkSphereSource()\n"
        evalString += "_sphere.SetThetaResolution(6)\n"
        evalString += "_sphere.SetPhiResolution(6)\n"
        evalString += "_sphere.SetRadius(0.5)"
        self.renderer.runString(evalString)

        # make tensor glyphs
        evalString = "_glyph = vtk.vtkTensorGlyph()\n"
        evalString += "_glyph.SetSource(_sphere.GetOutput())\n"
        evalString += "_glyph.SetInput(_extractGrid)\n"
        evalString += "_glyph.SetColorModeToScalars()\n"
        evalString += "_glyph.ScalingOn()\n"
        evalString += "_glyph.SetMaxScaleFactor(5.0)\n"
        evalString += "_glyph.SetScaleFactor(1.0)\n"
        evalString += "_glyph.ClampScalingOn()"
        self.renderer.runString(evalString)

        # make a stripper for faster rendering
        evalString = "_stripper = vtk.vtkStripper()\n"
        evalString += "_stripper.SetInput(_glyph.GetOutput())"
        self.renderer.runString(evalString)

        # make the normals of the data
        evalString = "_normals = vtk.vtkPolyDataNormals()\n"
        evalString += "_normals.SetInput(_stripper.GetOutput())"
        self.renderer.runString(evalString)

        # make the mapper for the data
        evalString = "_mapper = vtk.vtkPolyDataMapper()\n"
        evalString += "_mapper.SetInput(_normals.GetOutput())\n"
        evalString += "_mapper.SetLookupTable(_lut)\n"
        evalString += "_mapper.SetScalarRange(_extractScalarRange)"
        self.renderer.runString(evalString)

        # make the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.runString(evalString)

        # add the actor
        self.renderer.runString("_renderer.AddActor(_actor)")

        # set up the text properties for nice text
        evalString = "_textProp = vtk.vtkTextProperty()\n"
        evalString += "_textProp.SetFontFamilyToArial()\n"
        evalString += "_textProp.BoldOff()\n"
        evalString += "_textProp.ItalicOff()\n"
        evalString += "_textProp.ShadowOff()\n"
        evalString += "_textProp.SetColor(0.0, 0.0, 0.0)"
        self.renderer.runString(evalString)

        # if a title is set, put it in here
        if self.title is not None:
            # make a title
            evalString = "_title = vtk.vtkTextMapper()\n"
            evalString += "_title.SetInput(\"%s\")\n" % self.title

            # make the title text use the text properties
            evalString += "_titleProp = _title.GetTextProperty()\n"
            evalString += "_titleProp.ShallowCopy(_textProp)\n"
            evalString += "_titleProp.SetJustificationToCentered()\n"
            evalString += "_titleProp.SetVerticalJustificationToTop()\n"
            evalString += "_titleProp.SetFontSize(20)\n"
            evalString += "_titleProp.BoldOn()\n"

            # make the actor for the title
            evalString += "_titleActor = vtk.vtkTextActor()\n"
            evalString += "_titleActor.SetMapper(_title)\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetCoordinateSystemToNormalizedDisplay()\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetValue(0.5, 0.95)"
            self.renderer.runString(evalString)

            # add to the renderer
            evalString = "_renderer.AddActor(_titleActor)"
            self.renderer.runString(evalString)

        # add a scalar bar
        evalString = "_scalarBar = vtk.vtkScalarBarActor()\n"
        evalString += "_scalarBar.SetLookupTable(_lut)\n"
        evalString += "_scalarBar.SetWidth(0.1)\n"
        evalString += "_scalarBar.SetHeight(0.8)\n"
        evalString += "_scalarBar.SetPosition(0.9, 0.15)"
        self.renderer.runString(evalString)

        # set up the label text properties 
        evalString = "_scalarBarTextProp = _scalarBar.GetLabelTextProperty()\n"
        evalString += "_scalarBarTextProp.ShallowCopy(_textProp)\n"
        evalString += "_scalarBarTextProp.SetFontSize(10)\n"

        evalString += "_renderer.AddActor(_scalarBar)"
        self.renderer.runString(evalString)

        return

class IsosurfacePlot(Plot):
    """
    Isosurface plot
    """
    def __init__(self, scene):
        """
        Initialisation of the IsosurfacePlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        debugMsg("Called IsosurfacePlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer
        self.renderer.addToInitStack("# IsosurfacePlot.__init__()")

        # labels and stuff
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        # how many contours?
        self.numContours = 5

        # contour range
        self.contMin = None
        self.contMax = None

        # default values for fname and format
        self.fname = None
        self.format = None

        # add the plot to the scene
        scene.add(self)

    def setData(self, *dataList, **options):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple

        @param options: Dictionary of keyword options to the method
        @type options: dict
        """
        debugMsg("Called setData() in IsosurfacePlot()")

        self.renderer.runString("# IsosurfacePlot.setData()")

        # process the options, if any
        ## fname
        if options.has_key('fname'):
            fname = options['fname']
        else:
            fname = None
        ## format
        if options.has_key('format'):
            format = options['format']
        else:
            format = None

        # do a quick sanity check on the inputs
        if fname is None or format is None:
            raise ValueError, "You must supply an input file and its format"

        # we want to pass this info around
        self.fname = fname
        self.format = format

        # check to see if the file exists
        if not os.path.exists(fname):
            raise SystemError, "File %s not found" % fname

        if format == 'vtk':
            # read old-style vtk files
            evalString = "_reader = vtk.vtkUnstructuredGridReader()\n"
        elif format == 'vtk-xml':
            # read vtk xml files
            evalString = "_reader = vtk.vtkXMLUnstructuredGridReader()\n"
        else:
            # barf
            raise ValueError, "Unknown format.  I got %s" % format

        evalString += "_reader.SetFileName(\"%s\")\n" % fname
        evalString += "_reader.Update()"
        self.renderer.runString(evalString)

        # need to do a delaunay 3D here to get decent looking isosurfaces
        evalString = "_del3D = vtk.vtkDelaunay3D()\n"
        evalString += "_del3D.SetInput(_reader.GetOutput())\n"
        evalString += "_del3D.SetOffset(2.5)\n"
        evalString += "_del3D.SetTolerance(0.001)\n"
        evalString += "_del3D.SetAlpha(0.0)"
        self.renderer.runString(evalString)

        # get the model centre and bounds
        evalString = "_centre = _reader.GetOutput().GetCenter()\n"
        evalString += "_bounds = _reader.GetOutput().GetBounds()"
        self.renderer.runString(evalString)

    def render(self):
        """
        Does IsosurfacePlot object specific (pre)rendering stuff
        """
        debugMsg("Called IsosurfacePlot.render()")

        self.renderer.runString("# IsosurfacePlot.render()")

        # set up a contour filter
        evalString = "_cont = vtk.vtkContourGrid()\n"
        evalString += "_cont.SetInput(_del3D.GetOutput())\n"

        # if contMin and contMax are or aren't set then handle the different
        # situations
        if self.contMin is not None and self.contMax is not None:
            evalString += "_cont.GenerateValues(%d, %f, %f)\n" % \
                    (self.numContours, self.contMin, self.contMax)
        elif self.contMin is not None and self.contMax is None:
            evalString += "(_contMin, _contMax) = _reader.GetOutput()."
            evalString += "GetPointData().GetScalars().GetRange()\n"
            evalString += "_cont.GenerateValues(%d, %f, _contMax)\n" % \
                    (self.numContours, self.contMin)
        elif self.contMin is None and self.contMax is not None:
            evalString += "(_contMin, _contMax) = _reader.GetOutput()."
            evalString += "GetPointData().GetScalars().GetRange()\n"
            evalString += "_cont.GenerateValues(%d, _contMin, %f)\n" % \
                    (self.numContours, self.contMax)
        elif self.contMin is None and self.contMax is None:
            evalString += "(_contMin, _contMax) = _reader.GetOutput()."
            evalString += "GetPointData().GetScalars().GetRange()\n"
            evalString += "_cont.GenerateValues(%d, _contMin, _contMax)\n" % \
                    (self.numContours)
        else:
            # barf, really shouldn't have got here
            raise ValueError, \
                    "Major problems in IsosurfacePlot: contMin and contMax"

        evalString += "_cont.GenerateValues(5, 0.25, 0.75)\n"
        evalString += "_cont.ComputeScalarsOn()"
        self.renderer.runString(evalString)

        # set up the mapper
        evalString = "_mapper = vtk.vtkDataSetMapper()\n"
        evalString += "_mapper.SetInput(_cont.GetOutput())\n"
        evalString += "_mapper.ScalarVisibilityOn()"
        self.renderer.runString(evalString)

        # set up the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.runString(evalString)

        # add to the renderer
        evalString = "_renderer.AddActor(_actor)"
        self.renderer.runString(evalString)

        # set up the text properties for nice text
        evalString = "_font_size = 18\n"
        evalString += "_textProp = vtk.vtkTextProperty()\n"
        evalString += "_textProp.SetFontSize(_font_size)\n"
        evalString += "_textProp.SetFontFamilyToArial()\n"
        evalString += "_textProp.BoldOff()\n"
        evalString += "_textProp.ItalicOff()\n"
        evalString += "_textProp.ShadowOff()\n"
        evalString += "_textProp.SetColor(0.0, 0.0, 0.0)"
        self.renderer.runString(evalString)

        # if a title is set, put it in here
        if self.title is not None:
            # make a title
            evalString = "_title = vtk.vtkTextMapper()\n"
            evalString += "_title.SetInput(\"%s\")\n" % self.title

            # make the title text use the text properties
            evalString += "_titleProp = _title.GetTextProperty()\n"
            evalString += "_titleProp.ShallowCopy(_textProp)\n"
            evalString += "_titleProp.SetJustificationToCentered()\n"
            evalString += "_titleProp.SetVerticalJustificationToTop()\n"

            # make the actor for the title
            evalString += "_titleActor = vtk.vtkTextActor()\n"
            evalString += "_titleActor.SetMapper(_title)\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetCoordinateSystemToNormalizedDisplay()\n"
            evalString += "_titleActor.GetPositionCoordinate()."
            evalString += "SetValue(0.5, 0.95)"
            self.renderer.runString(evalString)

            # add to the renderer
            evalString = "_renderer.AddActor(_titleActor)"
            self.renderer.runString(evalString)

        # put an outline around the data
        evalString = "_outline = vtk.vtkOutlineSource()\n"
        evalString += "_outline.SetBounds(_bounds)\n"

        # make its mapper
        evalString += "_outlineMapper = vtk.vtkPolyDataMapper()\n"
        evalString += "_outlineMapper.SetInput(_outline.GetOutput())\n"

        # make its actor
        evalString += "_outlineActor = vtk.vtkActor()\n"
        evalString += "_outlineActor.SetMapper(_outlineMapper)\n"
        evalString += "_outlineActor.GetProperty().SetColor(0,0,0)"
        self.renderer.runString(evalString)

        # add to the renderer
        evalString = "_renderer.AddActor(_outlineActor)"
        self.renderer.runString(evalString)

        # make a lookup table for the colour map and invert it (colours look
        # better when it's inverted)
        evalString = "_lut = vtk.vtkLookupTable()\n"
        evalString += "_refLut = vtk.vtkLookupTable()\n"
        evalString += "_lut.Build()\n"
        evalString += "_refLut.Build()\n"
        evalString += "for _j in range(256):\n"
        evalString += "    _lut.SetTableValue(_j, "
        evalString += "_refLut.GetTableValue(255-_j))"
        self.renderer.runString(evalString)

        # add some axes
        evalString = "_axes = vtk.vtkCubeAxesActor2D()\n"
        evalString += "_axes.SetInput(_reader.GetOutput())\n"
        evalString += "_axes.SetCamera(_renderer.GetActiveCamera())\n"
        evalString += "_axes.SetLabelFormat(\"%6.4g\")\n"
        evalString += "_axes.SetFlyModeToOuterEdges()\n"
        evalString += "_axes.SetFontFactor(0.8)\n"
        evalString += "_axes.SetAxisTitleTextProperty(_textProp)\n"
        evalString += "_axes.SetAxisLabelTextProperty(_textProp)\n"
        ### xlabel
        if self.xlabel is not None:
            evalString += "_axes.SetXLabel(\"%s\")\n" % self.xlabel
        else:
            evalString += "_axes.SetXLabel(\"\")\n"
        ### ylabel
        if self.ylabel is not None:
            evalString += "_axes.SetYLabel(\"%s\")\n" % self.ylabel
        else:
            evalString += "_axes.SetYLabel(\"\")\n"
        ### zlabel
        if self.zlabel is not None:
            evalString += "_axes.SetZLabel(\"%s\")\n" % self.zlabel
        else:
            evalString += "_axes.SetZLabel(\"\")\n"
        evalString += "_axes.SetNumberOfLabels(5)\n"
        evalString += "_axes.GetProperty().SetColor(0,0,0)"
        self.renderer.runString(evalString)

        # add to the renderer
        evalString = "_renderer.AddActor(_axes)"
        self.renderer.runString(evalString)

        # play around with lighting
        evalString = "_light1 = vtk.vtkLight()\n"
        evalString += "_light1.SetFocalPoint(_centre)\n"
        evalString += "_light1.SetPosition(_centre[0]-_bounds[1], "
        evalString += "_centre[1]-_bounds[3], _centre[2]+_bounds[5])\n"
        evalString += "_renderer.AddLight(_light1)\n"
        evalString += "_light2 = vtk.vtkLight()\n"
        evalString += "_light2.SetFocalPoint(_centre)\n"
        evalString += "_light2.SetPosition(_centre[0]+_bounds[1], "
        evalString += "_centre[1]+_bounds[3], _centre[2]-_bounds[5])\n"
        evalString += "_renderer.AddLight(_light2)"
        self.renderer.runString(evalString)

        # this shouldn't be here!!!!
        self.renderer.runString("_renderer.SetBackground(1,1,1)")

        return

class LinePlot(Plot):
    """
    Line plot
    """
    def __init__(self, scene):
        """
        Initialisation of the LinePlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        debugMsg("Called LinePlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer
        self.renderer.addToInitStack("# LinePlot.__init__()")
        self.renderer.addToInitStack("_plot = vtk.vtkXYPlotActor()")

        # offset the data in the lineplot?
        self.offset = False

        # add the plot to the scene
        scene.add(self)

    def setData(self, *dataList, **options):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in LinePlot()")

        self.renderer.runString("# LinePlot.setData()")

        # if offset is used, process it
        if options.has_key('offset'):
            self.offset = options['offset']
        else:
            self.offset = False

        # do some sanity checking on the data
        for i in range(len(dataList)):
            if len(dataList[0]) != len(dataList[i]):
                raise ValueError, "Input vectors must all be the same length"

        # if have more than one array to plot, the first one is the x data
        if len(dataList) > 1:
            xData = dataList[0]
            ## generate the evalString for the x data
            evalString = "_x = array(["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s])" % xData[-1]
            # give it to the renderer
            self.renderer.runString(evalString)
            # don't need the first element of the dataList, so get rid of it
            dataList = dataList[1:]
            # if only have one array input, then autogenerate xData
        elif len(dataList) == 1:
            xData = range(1, len(dataList[0])+1)
            if len(xData) != len(dataList[0]):
                errorString = "Autogenerated xData array length not "
                errorString += "equal to input array length"
                raise ValueError, errorString
            ## generate the evalString for the x data
            evalString = "_x = array(["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s])" % xData[-1]
            # send it to the renderer
            self.renderer.runString(evalString)

        # set up the vtkDataArray object for the x data
        self.renderer.runString(
                "_xData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)")
        self.renderer.runString(
                "_xData.SetNumberOfTuples(len(_x))")

        ## now to handle the y data

        # now to add my dodgy hack until I have a decent way of sharing data
        # objects around properly
        for i in range(len(dataList)):
            evalString = "_y%d = array([" % i
            data = dataList[i]
            # check that the data here is a 1-D array
            if len(data.shape) != 1:
                raise ValueError, "Can only handle 1D arrays at present"

            for j in range(len(data)-1):
                evalString += "%s, " % data[j]
            evalString += "%s])" % data[-1]
            self.renderer.runString(evalString)

        # if offset is true then shift the data
        if self.offset:
            # concatenate the data
            evalString = "_yAll = concatenate(["
            for i in range(len(dataList)-1):
                evalString += "_y%d," % i
            evalString += "_y%d])" % int(len(dataList)-1)
            self.renderer.runString(evalString)

            # grab the min and max values
            self.renderer.runString("_yMax = max(_yAll)")
            self.renderer.runString("_yMin = min(_yAll)")

            # keep the data apart a bit
            self.renderer.runString("_const = 0.1*(_yMax - _yMin)")

            # now shift the data
            self.renderer.runString("_shift = _yMax - _yMin + _const")
            for i in range(len(dataList)):
                evalString = "_y%d = _y%d + %d*_shift" % (i, i, i)
                self.renderer.runString(evalString)

        # set up the vtkDataArray objects
        for i in range(len(dataList)):
            evalString = \
            "_y%dData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)\n" % i
            evalString += "_y%dData.SetNumberOfTuples(len(_y%d))" % (i, i)
            self.renderer.runString(evalString)

        ## x data
        # put the data into the data arrays
        self.renderer.runString("for i in range(len(_x)):")
        # need to be careful here to remember to indent the code properly
        evalString = "    _xData.SetTuple1(i,_x[i])"
        self.renderer.runString(evalString)

        ## y data
        # put the data into the data arrays
        self.renderer.runString("for i in range(len(_x)):")
        # need to be careful here to remember to indent the code properly
        for i in range(len(dataList)):
            evalString = "    _y%dData.SetTuple1(i,_y%d[i])" % (i, i)
            self.renderer.runString(evalString)

        for i in range(len(dataList)):
            # create the field data object
            evalString = "_fieldData%d = vtk.vtkFieldData()" % i
            self.renderer.runString(evalString)
            evalString = "_fieldData%d.AllocateArrays(2)" % i
            self.renderer.runString(evalString)
            evalString = "_fieldData%d.AddArray(_xData)" % i
            self.renderer.runString(evalString)
            evalString = "_fieldData%d.AddArray(_y%dData)" % (i, i)
            self.renderer.runString(evalString)

        for i in range(len(dataList)):
            # now put the field data into a data object
            evalString = "_dataObject%d = vtk.vtkDataObject()\n" % i
            evalString += "_dataObject%d.SetFieldData(_fieldData%d)\n" % (i, i)

            # the actor should be set up, so add the data object to the actor
            evalString += "_plot.AddDataObjectInput(_dataObject%d)" % i
            self.renderer.runString(evalString)

        # tell the actor to use the x values for the x values (rather than
        # the index)
        self.renderer.runString("_plot.SetXValuesToValue()")

        # set which parts of the data object are to be used for which axis
        self.renderer.runString("_plot.SetDataObjectXComponent(0,0)")
        for i in range(len(dataList)):
            evalString = "_plot.SetDataObjectYComponent(%d,1)" % i
            self.renderer.runString(evalString)

        # note: am ignoring zlabels as vtk xyPlot doesn't support that
        # dimension for line plots (I'll have to do something a lot more
        # funky if I want that kind of functionality)

        # should this be here or elsewhere?
        evalString = "_plot.GetXAxisActor2D().GetProperty().SetColor(0, 0, 0)\n"
        evalString += "_plot.GetYAxisActor2D().GetProperty().SetColor(0, 0, 0)\n"
        evalString += "_renderer.SetBackground(1.0, 1.0, 1.0)"
        self.renderer.runString(evalString)

        # set up the lookup table for the appropriate range of colours
        evalString = "_lut = vtk.vtkLookupTable()\n"
        evalString += "_lut.Build()\n"
        evalString += "_colours = []\n"
        # need to handle the case when only have one element in dataList
        if len(dataList) == 1:
            evalString += "_colours.append(_lut.GetColor(0))\n"
        else:
            for i in range(len(dataList)):
                evalString += "_colours.append(_lut.GetColor(%f))\n" \
                        % (float(i)/float(len(dataList)-1),)
        self.renderer.runString(evalString)
    
        # change the colour of the separate lines
        for i in range(len(dataList)):
            evalString = "_plot.SetPlotColor(%d, _colours[%d][0], " % (i, i)
            evalString += "_colours[%d][1], _colours[%d][2])" % (i, i)
            self.renderer.runString(evalString)

        # make sure the plot is a decent size
        # the size of the actor should be 80% of the render window
        evalString = "_plot.SetPosition(0.1, 0.1)\n" # (0.1 = (1.0 - 0.8)/2)
        evalString += "_plot.SetWidth(0.8)\n"
        evalString += "_plot.SetHeight(0.8)"
        self.renderer.runString(evalString)

        return

    def render(self):
        """
        Does LinePlot object specific (pre)rendering stuff
        """
        debugMsg("Called LinePlot.render()")

        self.renderer.runString("# LinePlot.render()")
        self.renderer.runString("_renderer.AddActor2D(_plot)")

        # set the title if set
        if self.title is not None:
            evalString = "_plot.SetTitle(\'%s\')" % self.title
            self.renderer.runString(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_plot.SetXTitle(\'%s\')" % self.xlabel
            self.renderer.runString(evalString)

        # if an ylabel is set, add it
        if self.ylabel is not None:
            evalString = "_plot.SetYTitle(\'%s\')" % self.ylabel
            self.renderer.runString(evalString)

        return

class OffsetPlot(Plot):
    """
    Offset plot
    """
    def __init__(self, scene):
        """
        Initialisation of the OffsetPlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        debugMsg("Called OffsetPlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer
        self.renderer.addToInitStack("# OffsetPlot.__init__()")
        self.renderer.addToInitStack("_plot = vtk.vtkXYPlotActor()")

        self.title = None
        self.xlabel = None
        self.ylabel = None

        # the extra separation between curves (user set)
        self.sep = None

        # add the plot to the scene
        scene.add(self)

    def setData(self, *dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in OffsetPlot()")

        self.renderer.runString("# OffsetPlot.setData()")

        # do some sanity checking on the data
        if len(dataList) > 3 or len(dataList) < 1:
            raise ValueError, "Must have either one, two or three input arrays"

        # the data is y values located at different x positions, changing
        # over time, so the normal x-direction is t, the normal y direction
        # is both x and y; y basically being offset by the x values
        # therefore will refer to tData, xData and yData

        # compare the shapes of the input vectors.
        # assume that the first one is the t data, and that the first
        # dimension of the second one is the same length as the t data
        # length
        if len(dataList) == 1:
            yData = dataList[0]
        elif len(dataList) == 2:
            tData = dataList[0]
            yData = dataList[1]
            if tData.shape[0] != yData.shape[0]:
                raise ValueError, "Input arrays don't have the correct shape"
        elif len(dataList) == 3:
            tData = dataList[0]
            xData = dataList[1]
            yData = dataList[2]
            if tData.shape[0] != yData.shape[0]:
                raise ValueError, \
                    "First dim of third arg doesn't agree with first arg"
            if len(yData.shape) == 1:
                if xData.shape[0] != 1:
                    raise ValueError, \
                       "Second arg must be a scalar when third arg is a vector"
            elif len(yData.shape) == 2:
                if xData.shape[0] != yData.shape[1]:
                    raise ValueError, \
                       "Second dim of third arg doesn't agree with second arg"

        # if only have one array input, then autogenerate tData
        if len(dataList) == 1:
            tData = range(1, len(dataList[0])+1)
            if len(tData) != len(dataList[0]):
                errorString = "Autogenerated xData array length not "
                errorString += "equal to input array length"
                raise ValueError, errorString
            ## generate the evalString for the x data
            evalString = "_t = array(["
            for j in range(len(tData)-1):
                evalString += "%s, " % tData[j]
            evalString += "%s])" % tData[-1]
            # send it to the renderer
            self.renderer.runString(evalString)
        # if have two arrays to plot, the first one is the t data
        elif len(dataList) == 2:
            tData = dataList[0]
            ## generate the evalString for the x data
            evalString = "_t = array(["
            for j in range(len(tData)-1):
                evalString += "%s, " % tData[j]
            evalString += "%s])" % tData[-1]
            # give it to the renderer
            self.renderer.runString(evalString)
            # don't need the first element of the dataList, so get rid of it
            dataList = dataList[1:]
        elif len(dataList) == 3:
            ## generate the evalString for the t data
            evalString = "_t = array(["
            for j in range(len(tData)-1):
                evalString += "%s, " % tData[j]
            evalString += "%s])" % tData[-1]
            # give it to the renderer
            self.renderer.runString(evalString)
            ## generate the evalString for the x data
            evalString = "_x = array(["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s])" % xData[-1]
            # give it to the renderer
            self.renderer.runString(evalString)
        else:
            # shouldn't get to here, but raise an error anyway
            raise ValueError, "Incorrect number of arguments"

        # set up the vtkDataArray object for the t data
        self.renderer.runString(
                "_tData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)")
        self.renderer.runString(
                "_tData.SetNumberOfTuples(len(_t))")

        ## now to handle the y data
        if len(yData.shape) == 1:
            dataLen = 1
        elif len(yData.shape) == 2:
            dataLen = yData.shape[1]
        else:
            raise ValueError, \
                    "The last setData argument has the incorrect shape"

        # now to add my dodgy hack until I have a decent way of sharing data
        # objects around properly
        for i in range(dataLen):
            evalString = "_y%d = array([" % i
            if len(yData.shape) == 1:
                data = yData
            else:
                data = yData[:, i]
            # check that the data here is a 1-D array
            if len(data.shape) != 1:
                raise ValueError, "Can only handle 1D arrays at present"

            for j in range(len(data)-1):
                evalString += "%s, " % data[j]
            evalString += "%s])" % data[-1]
            self.renderer.runString(evalString)

        # concatenate the data
        evalString = "_yAll = concatenate(["
        for i in range(dataLen-1):
            evalString += "_y%d," % i
        evalString += "_y%d])" % int(dataLen-1)
        self.renderer.runString(evalString)

        # grab the min and max values
        self.renderer.runString("_yMax = max(_yAll)")
        self.renderer.runString("_yMin = min(_yAll)")

        # keep the data apart a bit
        if self.sep is None:
            self.renderer.runString("_const = 0.1*(_yMax - _yMin)")
        else:
            evalString = "_const = %f" % self.sep
            self.renderer.runString(evalString)

        # behave differently with the shift if we have xData as to not
        if len(dataList) == 3:
            # this is for when we have xData
            self.renderer.runString("_yMaxAbs = max(abs(_yAll))")
            # calculate the minimum delta x
            x1 = xData[:-1]
            x2 = xData[1:]
            minDeltax = min(x2 - x1)
            evalString = "_scale = %f/(2.0*_yMaxAbs)" % minDeltax
            self.renderer.runString(evalString)

            for i in range(dataLen):
                evalString = "_y%d = _scale*_y%d + _x[%d]" % (i, i, i)
                self.renderer.runString(evalString)
        else:
            # shift the data up
            self.renderer.runString("_shift = _yMax - _yMin + _const")

            for i in range(dataLen):
                evalString = "_y%d = _y%d + %f*_shift" % (i, i, i)
                self.renderer.runString(evalString)

        # set up the vtkDataArray objects
        for i in range(dataLen):
            evalString = \
            "_y%dData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)\n" % i
            evalString += "_y%dData.SetNumberOfTuples(len(_y%d))" % (i, i)
            self.renderer.runString(evalString)

        ## t data
        # put the data into the data arrays
        self.renderer.runString("for i in range(len(_t)):")
        # need to be careful here to remember to indent the code properly
        evalString = "    _tData.SetTuple1(i,_t[i])"
        self.renderer.runString(evalString)

        ## y data
        # put the data into the data arrays
        self.renderer.runString("for i in range(len(_t)):")
        # need to be careful here to remember to indent the code properly
        for i in range(dataLen):
            evalString = "    _y%dData.SetTuple1(i,_y%d[i])" % (i, i)
            self.renderer.runString(evalString)

        for i in range(dataLen):
            # create the field data object
            evalString = "_fieldData%d = vtk.vtkFieldData()" % i
            self.renderer.runString(evalString)
            evalString = "_fieldData%d.AllocateArrays(2)" % i
            self.renderer.runString(evalString)
            evalString = "_fieldData%d.AddArray(_tData)" % i
            self.renderer.runString(evalString)
            evalString = "_fieldData%d.AddArray(_y%dData)" % (i, i)
            self.renderer.runString(evalString)

        for i in range(dataLen):
            # now put the field data into a data object
            evalString = "_dataObject%d = vtk.vtkDataObject()\n" % i
            evalString += "_dataObject%d.SetFieldData(_fieldData%d)\n" % (i, i)

            # the actor should be set up, so add the data object to the actor
            evalString += "_plot.AddDataObjectInput(_dataObject%d)" % i
            self.renderer.runString(evalString)

        # tell the actor to use the x values for the x values (rather than
        # the index)
        self.renderer.runString("_plot.SetXValuesToValue()")

        # set which parts of the data object are to be used for which axis
        self.renderer.runString("_plot.SetDataObjectXComponent(0,0)")
        for i in range(dataLen):
            evalString = "_plot.SetDataObjectYComponent(%d,1)" % i
            self.renderer.runString(evalString)

        # note: am ignoring zlabels as vtk xyPlot doesn't support that
        # dimension for line plots (I'll have to do something a lot more
        # funky if I want that kind of functionality)

        return

    def render(self):
        """
        Does OffsetPlot object specific (pre)rendering stuff
        """
        debugMsg("Called OffsetPlot.render()")

        self.renderer.runString("# OffsetPlot.render()")
        self.renderer.runString("_renderer.AddActor2D(_plot)")

        # set the title if set
        if self.title is not None:
            evalString = "_plot.SetTitle(\'%s\')" % self.title
            self.renderer.runString(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_plot.SetXTitle(\'%s\')" % self.xlabel
            self.renderer.runString(evalString)

        # if an ylabel is set, add it
        if self.ylabel is not None:
            evalString = "_plot.SetYTitle(\'%s\')" % self.ylabel
            self.renderer.runString(evalString)

        return

# vim: expandtab shiftwidth=4:

