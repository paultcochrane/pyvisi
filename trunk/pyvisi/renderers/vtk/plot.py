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
from Numeric import *

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

        self.renderer.addToEvalStack("# ArrowPlot.__init__()")

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

        # this is a really dodgy way to get the data into the renderer
        # I really have to find a better, more elegant way to do this
        
        # this is a bad, cut-and-paste way to code it, but it will get going
        # at least...
        # x data
        ## generate the evalString for the x data
        evalString = "_x = array(["
        for j in range(len(xData)-1):
            evalString += "%s, " % xData[j]
        evalString += "%s])" % xData[-1]
        # give it to the renderer
        self.renderer.addToEvalStack(evalString)

        # y data
        ## generate the evalString for the y data
        evalString = "_y = array(["
        for j in range(len(yData)-1):
            evalString += "%s, " % yData[j]
        evalString += "%s])" % yData[-1]
        # give it to the renderer
        self.renderer.addToEvalStack(evalString)

        # dx data
        ## generate the evalString for the dx data
        evalString = "_dx = array(["
        for j in range(len(dxData)-1):
            evalString += "%s, " % dxData[j]
        evalString += "%s])" % dxData[-1]
        # give it to the renderer
        self.renderer.addToEvalStack(evalString)

        # dy data
        ## generate the evalString for the dy data
        evalString = "_dy = array(["
        for j in range(len(dyData)-1):
            evalString += "%s, " % dyData[j]
        evalString += "%s])" % dyData[-1]
        # give it to the renderer
        self.renderer.addToEvalStack(evalString)

        # keep the number of points for future reference
        numPoints = len(xData)

        # construct the points data
        evalString = "_points = vtk.vtkPoints()\n"
        evalString += "_points.SetNumberOfPoints(%d)\n" % numPoints
        for j in range(numPoints):
            evalString += "_points.InsertPoint(%d, %f, %f, 0.0)\n" % \
                    (j, xData[j], yData[j])
        self.renderer.addToEvalStack(evalString)

        # construct the vectors
        evalString = "_vectors = vtk.vtkFloatArray()\n"
        evalString += "_vectors.SetNumberOfComponents(3)\n"
        evalString += "_vectors.SetNumberOfTuples(%d)\n" % numPoints
        evalString += "_vectors.SetName(\"vectors\")\n"
        for j in range(numPoints):
            evalString += "_vectors.InsertTuple3(%d, %f, %f, 0.0)\n" % \
                    (j, dxData[j], dyData[j])
        self.renderer.addToEvalStack(evalString)

        # construct the grid
        evalString = "_grid = vtk.vtkUnstructuredGrid()\n"
        evalString += "_grid.SetPoints(_points)\n"
        evalString += "_grid.GetPointData().AddArray(_vectors)\n"
        evalString += "_grid.GetPointData().SetActiveVectors(\"vectors\")"
        self.renderer.addToEvalStack(evalString)


    def render(self):
        """
        Does ArrowPlot specific rendering tasks
        """
        debugMsg("Called render() in ArrowPlot")
        self.renderer.addToEvalStack("# ArrowPlot.render()")

        # make the arrow source
        self.renderer.addToEvalStack("_arrow = vtk.vtkArrowSource()")

        # make the glyph
        evalString = "_glyph = vtk.vtkGlyph2D()\n"
        evalString += "_glyph.ScalingOn()\n"
        evalString += "_glyph.SetScaleModeToScaleByVector()\n"
        evalString += "_glyph.SetColorModeToColorByVector()\n"
        evalString += "_glyph.SetScaleFactor(0.5)\n"
        evalString += "_glyph.SetSource(_arrow.GetOutput())\n"
        evalString += "_glyph.SetInput(_grid)\n"
        evalString += "_glyph.ClampingOff()"
        self.renderer.addToEvalStack(evalString)

        # set up a stripper for faster rendering
        evalString = "_stripper = vtk.vtkStripper()\n"
        evalString += "_stripper.SetInput(_glyph.GetOutput())"
        self.renderer.addToEvalStack(evalString)

        # get the maximum norm of the data
        evalString = "_maxNorm = _grid.GetPointData().GetVectors().GetMaxNorm()"
        self.renderer.addToEvalStack(evalString)

        # set up the mapper
        evalString = "_mapper = vtk.vtkPolyDataMapper()\n"
        evalString += "_mapper.SetInput(_stripper.GetOutput())\n"
        evalString += "_mapper.SetScalarRange(0, _maxNorm)"
        self.renderer.addToEvalStack(evalString)

        # set up the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.addToEvalStack(evalString)

        # add the actor
        self.renderer.addToEvalStack("_renderer.AddActor(_actor)")

        # set the title if set
        if self.title is not None:
            # text properties
            evalString = "_font_size = 18\n"  # this will need to be an option!!
            evalString += "_textProp = vtk.vtkTextProperty()\n"
            evalString += "_textProp.SetFontSize(_font_size)\n"
            evalString += "_textProp.SetFontFamilyToArial()\n"
            evalString += "_textProp.BoldOff()\n"
            evalString += "_textProp.ItalicOff()\n"
            evalString += "_textProp.ShadowOff()\n"
            #evalString += "_textProp.SetColor(0,0,0)\n"
        
            # add a title
            evalString += "_titleMapper = vtk.vtkTextMapper()\n"
            evalString += "_titleMapper.SetInput(\"%s\")\n" % self.title
            
            evalString += "_titleProp = _titleMapper.GetTextProperty()\n"
            evalString += "_titleProp.ShallowCopy(_textProp)\n"
            evalString += "_titleProp.SetJustificationToCentered()\n"
            evalString += "_titleProp.SetVerticalJustificationToTop()\n"
            
            # set up the text actor
            evalString += "_titleActor = vtk.vtkTextActor()\n"
            evalString += "_titleActor.SetMapper(_titleMapper)\n"
            evalString += "_titleActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()\n"
            evalString += "_titleActor.GetPositionCoordinate().SetValue(0.5, 0.95)\n"

            evalString += "_renderer.AddActor(_titleActor)"
            self.renderer.addToEvalStack(evalString)

        # set up some axes
        evalString = "_axes = vtk.vtkCubeAxesActor2D()\n"
        evalString += "_axes.SetCamera(_renderer.GetActiveCamera())\n"
        evalString += "_axes.SetFlyModeToOuterEdges()\n"
        evalString += "_axes.SetBounds(min(_x), max(_x)+_maxNorm, min(_y), max(_y)+_maxNorm, 0, 0)\n"

        if self.xlabel is None:
            evalString += "_axes.SetXLabel(\"\")\n"
        else:
            evalString += "_axes.SetXLabel(\"%s\")\n" % self.xlabel

        if self.ylabel is None:
            evalString += "_axes.SetYLabel(\"\")\n"
        else:
            evalString += "_axes.SetYLabel(\"%s\")\n" % self.ylabel

        evalString += "_axes.SetZLabel(\"\")\n"
        evalString += "_axes.YAxisVisibilityOff()"  # but this is the z axis!!
        self.renderer.addToEvalStack(evalString)

        # add the axes to the renderer
        self.renderer.addToEvalStack("_renderer.AddActor(_axes)")

        # reset the camera, will make things look nicer
        ### is this the right place to put this???
        self.renderer.addToEvalStack("_renderer.ResetCamera()")

        return

class BallPlot(Plot):
    """
    Ball plot
    """
    def __init__(self, scene):
        debugMsg("Called BallPlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer

        self.renderer.addToEvalStack("# BallPlot.__init__()")

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
        self.renderer.addToEvalStack("# BallPlot.setData()")

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
            elif colors is None:
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
                self.renderer.addToEvalStack(evalString)
            elif format == "vtk":
                debugMsg("Using old-style vtk file as input")
                # create the reader of the file
                evalString = "_reader = vtk.vtkUnstructuredGridReader()\n"
                evalString += "_reader.SetFileName(\"%s\")\n" % fname
                evalString += "_reader.Update()"
                self.renderer.addToEvalStack(evalString)

            # read the output to an unstructured grid
            self.renderer.addToEvalStack("_grid = _reader.GetOutput()")

            # note that these next few steps are only necessary in vtk 4.2,
            # 4.4 grab the data to use for the radii of the balls
            evalString = \
                    "_radii = _grid.GetPointData().GetScalars(\"%s\")" % \
                    radii
            self.renderer.addToEvalStack(evalString)
    
            # grab the data to use for colouring the balls
            evalString = \
                    "_colours = _grid.GetPointData().GetScalars(\"%s\")" % \
                    colors
            self.renderer.addToEvalStack(evalString)
    
            # now work out the number of tags, and their values
            evalString = "_numPoints = _colours.GetNumberOfTuples()\n"
            evalString += "_valueDict = {}\n"
            evalString += "for i in range(_numPoints):\n"
            evalString += "    _colourValue = _colours.GetValue(i)\n"
            evalString += "    _valueDict[_colourValue] = 1\n"
    
            evalString += "_numColours = len(_valueDict.keys())\n"
    
            evalString += "_colourValues = _valueDict.keys()\n"
            evalString += "_colourValues.sort()"
            self.renderer.addToEvalStack(evalString)
    
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
            self.renderer.addToEvalStack(evalString)
    
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
            self.renderer.addToEvalStack(evalString)
    
            # add the data array to the grid
            evalString = "_grid.GetPointData().AddArray(_data)\n"
    
            # make the data the active scalars
            evalString += "_grid.GetPointData().SetActiveScalars(\"data\")"
            self.renderer.addToEvalStack(evalString)

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
                evalString += "_points.InsertPoint(%d, %f, %f, %f)\n" %\
                        (i, point[0], point[1], point[2])
            self.renderer.addToEvalStack(evalString)

            # make the radii
            evalString = "_radii = vtk.vtkFloatArray()\n"
            evalString += "_radii.SetNumberOfComponents(1)\n"
            evalString += "_radii.SetNumberOfValues(%d)\n" % numPoints
            for i in range(numPoints):
                evalString += "_radii.InsertValue(%d, %f)\n" % (i, radii[i])
            self.renderer.addToEvalStack(evalString)

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

                tags = zeros(numPoints, typecode=Int)
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
            self.renderer.addToEvalStack(evalString)

            # now scale the tags
            scaledTags = zeros(numPoints, typecode=Float)
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
            self.renderer.addToEvalStack(evalString)

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
            self.renderer.addToEvalStack(evalString)

            # now construct the grid
            evalString = "_grid = vtk.vtkUnstructuredGrid()\n"
            evalString += "_grid.SetPoints(_points)\n"

            # add the data array to the grid
            evalString += "_grid.GetPointData().AddArray(_data)\n"

            # make the data the active scalars
            evalString += "_grid.GetPointData().SetActiveScalars(\"data\")\n"

            self.renderer.addToEvalStack(evalString)
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
        self.renderer.addToEvalStack("# BallPlot.render()")

        # to make sphere glyphs need a sphere source
        evalString = "_sphere = vtk.vtkSphereSource()\n"
        evalString += "_sphere.SetRadius(1.0)\n"
        evalString += "_sphere.SetThetaResolution(5)\n"
        evalString += "_sphere.SetPhiResolution(5)"
        self.renderer.addToEvalStack(evalString)

        # the spheres are 3D glyphs so set that up
        evalString = "_glyph = vtk.vtkGlyph3D()\n"
        evalString += "_glyph.ScalingOn()\n"
        evalString += "_glyph.SetScaleModeToScaleByScalar()\n"
        evalString += "_glyph.SetColorModeToColorByScalar()\n"
        evalString += "_glyph.SetScaleFactor(1.0)\n"
        evalString += "_glyph.SetInput(_grid)\n"
        evalString += "_glyph.SetSource(_sphere.GetOutput())\n"
        evalString += "_glyph.ClampingOff()"
        self.renderer.addToEvalStack(evalString)

        # set up a stripper (this will speed up rendering)
        evalString = "_stripper = vtk.vtkStripper()\n"
        evalString += "_stripper.SetInput(_glyph.GetOutput())"
        self.renderer.addToEvalStack(evalString)

        # set up the mapper
        evalString = "_mapper = vtk.vtkPolyDataMapper()\n"
        evalString += "_mapper.SetInput(_stripper.GetOutput())\n"
        evalString += "_mapper.ScalarVisibilityOn()\n"
        # note: this is for vtk 4.2, 4.4 (4.5 and above have a better
        # technique to colour the scalars, but that version isn't yet
        # standard, or in fact released)
        evalString += "_mapper.ColorByArrayComponent(\"data\", 2)\n"
        # should be done in setData()
        evalString += "_mapper.SetScalarRange(0, 1)"
        self.renderer.addToEvalStack(evalString)

        # set up the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.addToEvalStack(evalString)

        # add the actor to the scene
        self.renderer.addToEvalStack("_renderer.AddActor(_actor)")

        # set the title if set
        if self.title is not None:
            # text properties
            evalString = "_font_size = 14\n"  # this will need to be an option!!
            evalString += "_textProp = vtk.vtkTextProperty()\n"
            evalString += "_textProp.SetFontSize(_font_size)\n"
            evalString += "_textProp.SetFontFamilyToArial()\n"
            evalString += "_textProp.BoldOff()\n"
            evalString += "_textProp.ItalicOff()\n"
            evalString += "_textProp.ShadowOff()\n"
        
            # add a title
            evalString += "_titleMapper = vtk.vtkTextMapper()\n"
            evalString += "_titleMapper.SetInput(\"%s\")\n" % self.title
            
            evalString += "_titleProp = _titleMapper.GetTextProperty()\n"
            evalString += "_titleProp.ShallowCopy(_textProp)\n"
            evalString += "_titleProp.SetJustificationToCentered()\n"
            evalString += "_titleProp.SetVerticalJustificationToTop()\n"
            
            # set up the text actor
            evalString += "_titleActor = vtk.vtkTextActor()\n"
            evalString += "_titleActor.SetMapper(_titleMapper)\n"
            evalString += "_titleActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()\n"
            evalString += "_titleActor.GetPositionCoordinate().SetValue(0.5, 0.95)\n"

            evalString += "_renderer.AddActor(_titleActor)"
            self.renderer.addToEvalStack(evalString)

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
        self.renderer.addToEvalStack("# ContourPlot.setData()")

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
        for object in dataList:
            try:
                object.convertToNumArray()
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
                Z = dataList[0]
                X = Z.getDomain().getX()
            elif len(dataList) == 2:
                # first variable should be the domain, the second the data
                X = dataList[0]
                Z = dataList[1]
            else:
                errorString = \
                        "Expecting 1 or 2 elements in data list.  I got: %d" \
                        % len(dataList)
                raise ValueError, errorString

            # convert the data to numarray
            xData = X[0].convertToNumArray()
            yData = X[1].convertToNumArray()
            zData = Z.convertToNumArray()

            # pass the data through to the pyvisi renderer
            ### the x data
            evalString = "_x = array(["
            for i in range(len(xData)-1):
                evalString += "%s, " % xData[i]
            evalString += "%s])" % xData[-1]
            self.renderer.addToEvalStack(evalString)

            ### the y data
            evalString = "_y = array(["
            for i in range(len(yData)-1):
                evalString += "%s, " % yData[i]
            evalString += "%s])" % yData[-1]
            self.renderer.addToEvalStack(evalString)

            ### the z data
            evalString = "_z = array(["
            for i in range(len(zData)-1):
                evalString += "%s, " % zData[i]
            evalString += "%s])" % zData[-1]
            self.renderer.addToEvalStack(evalString)

            # calculate the max and min of the z data
            evalString = "_zMin = min(_z)\n"
            evalString += "_zMax = max(_z)"
            self.renderer.addToEvalStack(evalString)

            # create the points
            evalString = "_points = vtk.vtkPoints()\n"
            evalString += "_points.SetNumberOfPoints(len(_x))\n"
            evalString += "for i in range(len(_x)):\n"
            evalString += "    _points.InsertPoint(i, _x[i], _y[i], 0)"
            self.renderer.addToEvalStack(evalString)

            # create the data
            evalString = "_data = vtk.vtkFloatArray()\n"
            evalString += "_data.SetNumberOfComponents(1)\n"
            evalString += "_data.SetNumberOfValues(len(_z))\n"
            evalString += "for i in range(len(_z)):\n"
            evalString += "    _data.InsertValue(i, _z[i])"
            self.renderer.addToEvalStack(evalString)

            # set up the grid (it's polydata since we're doing a Delaunay2D)
            evalString = "_grid = vtk.vtkPolyData()\n"
            evalString += "_grid.SetPoints(_points)\n"
            evalString += "_grid.GetPointData().SetScalars(_data)"
            self.renderer.addToEvalStack(evalString)

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
                    raise ValueError,\
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
                raise ValueError, "x data array is not of correct shape: %s"%\
                        xData.shape

            if len(yData.shape) != 1:
                raise ValueError, "y data array is not of correct shape: %s"%\
                        yData.shape

            if len(zData.shape) != 2:
                raise ValueError, "z data array is not of correct shape: %s"%\
                        zData.shape

            # stringify the data to then pass to the renderer
            ### x data
            evalString = "_x = array(["
            for i in range(len(xData)-1):
                evalString += "%s, " % xData[i]
            evalString += "%s])" % xData[-1]
            self.renderer.addToEvalStack(evalString)

            ### y data
            evalString = "_y = array(["
            for i in range(len(yData)-1):
                evalString += "%s, " % yData[i]
            evalString += "%s])" % yData[-1]
            self.renderer.addToEvalStack(evalString)

            ### z data
            evalString = "_z = array(["
            for i in range(len(xData)):
                evalString += "["
                for j in range(len(yData)-1):
                    evalString += "%s, " % zData[i, j]
                evalString += "%s],\n" % zData[i, -1]
            evalString += "])"
            self.renderer.addToEvalStack(evalString)

            # calculate the min and max
            evalString = "_zMax = max(_z.flat)\n"
            evalString += "_zMin = min(_z.flat)"
            self.renderer.addToEvalStack(evalString)

            # create the points
            evalString = "_points = vtk.vtkPoints()\n"
            evalString += "_points.SetNumberOfPoints(len(_x)*len(_y))\n"
            evalString += "_count = 0\n"
            evalString += "for i in range(len(_x)):\n"
            evalString += "  for j in range(len(_y)):\n"
            evalString += "    _points.InsertPoint(_count, _x[i], _y[j], 0)\n"
            evalString += "    _count += 1"
            self.renderer.addToEvalStack(evalString)

            # create the data
            evalString = "_data = vtk.vtkFloatArray()\n"
            evalString += "_data.SetNumberOfComponents(1)\n"
            evalString += "_data.SetNumberOfValues(len(_x)*len(_y))\n"
            evalString += "_count = 0\n"
            evalString += "for i in range(len(_x)):\n"
            evalString += "  for j in range(len(_y)):\n"
            evalString += "    _data.InsertValue(_count, _z[i][j])\n"
            evalString += "    _count += 1"
            self.renderer.addToEvalStack(evalString)

            # set up the grid (it's polydata since we're doing a Delaunay2D)
            evalString = "_grid = vtk.vtkPolyData()\n"
            evalString += "_grid.SetPoints(_points)\n"
            evalString += "_grid.GetPointData().SetScalars(_data)"
            self.renderer.addToEvalStack(evalString)

        # run the stuff for when we're reading from file
        if fname is not None:
            # create the reader of the file
            evalString = "_reader = vtk.vtkXMLUnstructuredGridReader()\n"
            evalString += "_reader.SetFileName(\"%s\")\n" % fname
            evalString += "_reader.Update()"
            self.renderer.addToEvalStack(evalString)
    
            # read the output input an unstructured grid
            evalString = "_grid = _reader.GetOutput()\n"
            evalString += \
                    "_grid.GetPointData().SetActiveScalars(\"%s\")" % scalars
            self.renderer.addToEvalStack(evalString)
    
            # grab the range of scalars for appropriate scaling of the colourmap
            evalString = \
                "_scalarRange = _grid.GetPointData().GetScalars().GetRange()\n"
            evalString += "_scalarMin = _scalarRange[0]\n"
            evalString += "_scalarMax = _scalarRange[1]\n"
            self.renderer.addToEvalStack(evalString)

        return

    def render(self):
        """
        Does ContourPlot object specific (pre)rendering stuff
        """
        debugMsg("Called ContourPlot.render()")

        self.renderer.addToEvalStack("# ContourPlot.render()")

        # set up the lookup table and reverse the order of the colours
        evalString = "_lut = vtk.vtkLookupTable()\n"
        evalString += "_lut.Build()\n"
        evalString += "_refLut = vtk.vtkLookupTable()\n"
        evalString += "_refLut.Build()\n"
        evalString += "for i in range(256):\n"
        evalString += \
                "    _lut.SetTableValue(i, _refLut.GetTableValue(255-i))"
        self.renderer.addToEvalStack(evalString)

        if self.escriptData or self.otherData:
            # triangulate the data
            evalString = "_delaunay = vtk.vtkDelaunay2D()\n"
            evalString += "_delaunay.SetInput(_grid)\n"
            evalString += "_delaunay.SetTolerance(0.001)"
            self.renderer.addToEvalStack(evalString)

            # set up the mapper
            evalString = "_mapper = vtk.vtkPolyDataMapper()\n"
            evalString += "_mapper.SetInput(_delaunay.GetOutput())\n"
            evalString += "_mapper.SetLookupTable(_lut)\n"
            # note that zMin and zMax are evaluated in setData()
            evalString += "_mapper.SetScalarRange(_zMin, _zMax)"
            self.renderer.addToEvalStack(evalString)

        elif self.fname is not None:
            # set up the mapper
            evalString = "_mapper = vtk.vtkDataSetMapper()\n"
            evalString += "_mapper.SetInput(_grid)\n"
            evalString += "_mapper.ScalarVisibilityOn()\n"
            evalString += "_mapper.SetLookupTable(_lut)\n"
            evalString += "_mapper.SetScalarRange(_scalarMin, _scalarMax)"
            self.renderer.addToEvalStack(evalString)

        # set up the actor
        evalString = "_actor = vtk.vtkActor()\n"
        evalString += "_actor.SetMapper(_mapper)"
        self.renderer.addToEvalStack(evalString)

        # add the actor to the scene
        self.renderer.addToEvalStack("_renderer.AddActor(_actor)")

        # if the title or one of the labels is set, then set up the text
        # properties (I think this should come from the pyvisi Text() object
        # at some stage, but we'll hard code it here...)
        # I'll also need separate properties for axes, titles, labels etc...
        # but keep them all the same just to get this going
        if self.title is not None or\
                self.xlabel is not None or\
                self.ylabel is not None:
            evalString = "_font_size = 20\n"
            evalString += "_textProp = vtk.vtkTextProperty()\n"
            evalString += "_textProp.SetFontSize(_font_size)\n"
            evalString += "_textProp.SetFontFamilyToArial()\n"
            evalString += "_textProp.BoldOff()\n"
            evalString += "_textProp.ItalicOff()\n"
            evalString += "_textProp.ShadowOff()\n"
            self.renderer.addToEvalStack(evalString)

        # set the title if set
        if self.title is not None:
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
            evalString += "SetValue(0.5,0.95)\n"# this should be user-settable
            # add the actor to the scene
            evalString += "_renderer.AddActor(_titleActor)"
            self.renderer.addToEvalStack(evalString)

        # add the axes
        evalString = "_axes = vtk.vtkCubeAxesActor2D()\n"
        evalString += "_axes.SetInput(_grid)\n"
        evalString += "_axes.SetCamera(_renderer.GetActiveCamera())\n"
        evalString += "_axes.SetLabelFormat(\"%6.4g\")\n"
        evalString += "_axes.SetFlyModeToOuterEdges()\n"
        evalString += "_axes.SetFontFactor(0.8)\n"
        evalString += "_axes.SetAxisTitleTextProperty(_textProp)\n"
        evalString += "_axes.SetAxisLabelTextProperty(_textProp)\n"
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
        self.renderer.addToEvalStack(evalString)

        # add a scalar bar (need to make this an option somewhere!!)
        # I also need to add the ability for the user to set the values of
        # the various parameters set below, and some kind of logical
        # defaults similar to or the same as what I have below.
        evalString = "_scalarBar = vtk.vtkScalarBarActor()\n"
        evalString += "_scalarBar.SetLookupTable(_lut)\n"
        evalString += "_scalarBar.SetWidth(0.1)\n"
        evalString += "_scalarBar.SetHeight(0.7)\n"
        evalString += "_scalarBar.SetPosition(0.9, 0.2)\n"
        
        # add the scalar bar to the scene
        evalString += "_renderer.AddActor(_scalarBar)\n"
        self.renderer.addToEvalStack(evalString)

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

        self.renderer.addToEvalStack("# LinePlot.setData()")

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
            self.renderer.addToEvalStack(evalString)
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
            self.renderer.addToEvalStack(evalString)

        # set up the vtkDataArray object for the x data
        self.renderer.addToEvalStack(
                "_xData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)")
        self.renderer.addToEvalStack(
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
            self.renderer.addToEvalStack(evalString)

        # if offset is true then shift the data
        if self.offset:
            # concatenate the data
            evalString = "_yAll = concatenate(["
            for i in range(len(dataList)-1):
                evalString += "_y%d," % i
            evalString += "_y%d])" % int(len(dataList)-1)
            self.renderer.addToEvalStack(evalString)

            # grab the min and max values
            self.renderer.addToEvalStack("_yMax = max(_yAll)")
            self.renderer.addToEvalStack("_yMin = min(_yAll)")

            # keep the data apart a bit
            self.renderer.addToEvalStack("_const = 0.1*(_yMax - _yMin)")

            # now shift the data
            self.renderer.addToEvalStack("_shift = _yMax - _yMin + _const")
            for i in range(len(dataList)):
                evalString = "_y%d = _y%d + %d*_shift" % (i, i, i)
                self.renderer.addToEvalStack(evalString)

        # set up the vtkDataArray objects
        for i in range(len(dataList)):
            evalString = \
            "_y%dData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)\n" % i
            evalString += "_y%dData.SetNumberOfTuples(len(_y%d))" % (i, i)
            self.renderer.addToEvalStack(evalString)

        ## x data
        # put the data into the data arrays
        self.renderer.addToEvalStack("for i in range(len(_x)):")
        # need to be careful here to remember to indent the code properly
        evalString = "    _xData.SetTuple1(i,_x[i])"
        self.renderer.addToEvalStack(evalString)

        ## y data
        # put the data into the data arrays
        self.renderer.addToEvalStack("for i in range(len(_x)):")
        # need to be careful here to remember to indent the code properly
        for i in range(len(dataList)):
            evalString = "    _y%dData.SetTuple1(i,_y%d[i])" % (i, i)
            self.renderer.addToEvalStack(evalString)

        for i in range(len(dataList)):
            # create the field data object
            evalString = "_fieldData%d = vtk.vtkFieldData()" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AllocateArrays(2)" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AddArray(_xData)" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AddArray(_y%dData)" % (i, i)
            self.renderer.addToEvalStack(evalString)

        for i in range(len(dataList)):
            # now put the field data into a data object
            evalString = "_dataObject%d = vtk.vtkDataObject()\n" % i
            evalString += "_dataObject%d.SetFieldData(_fieldData%d)\n" % (i, i)

            # the actor should be set up, so add the data object to the actor
            evalString += "_plot.AddDataObjectInput(_dataObject%d)" % i
            self.renderer.addToEvalStack(evalString)

        # tell the actor to use the x values for the x values (rather than
        # the index)
        self.renderer.addToEvalStack("_plot.SetXValuesToValue()")

        # set which parts of the data object are to be used for which axis
        self.renderer.addToEvalStack("_plot.SetDataObjectXComponent(0,0)")
        for i in range(len(dataList)):
            evalString = "_plot.SetDataObjectYComponent(%d,1)" % i
            self.renderer.addToEvalStack(evalString)

        # note: am ignoring zlabels as vtk xyPlot doesn't support that
        # dimension for line plots (I'll have to do something a lot more
        # funky if I want that kind of functionality)

        # should this be here or elsewhere?
        evalString = "_plot.GetXAxisActor2D().GetProperty().SetColor(0, 0, 0)\n"
        evalString += "_plot.GetYAxisActor2D().GetProperty().SetColor(0, 0, 0)\n"
        evalString += "_renderer.SetBackground(1.0, 1.0, 1.0)"
        self.renderer.addToEvalStack(evalString)

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
        self.renderer.addToEvalStack(evalString)
    
        # change the colour of the separate lines
        for i in range(len(dataList)):
            evalString = "_plot.SetPlotColor(%d, _colours[%d][0], " % (i, i)
            evalString += "_colours[%d][1], _colours[%d][2])" % (i, i)
            self.renderer.addToEvalStack(evalString)

        # make sure the plot is a decent size
        # the size of the actor should be 80% of the render window
        evalString = "_plot.SetPosition(0.1, 0.1)\n" # (0.1 = (1.0 - 0.8)/2)
        evalString += "_plot.SetWidth(0.8)\n"
        evalString += "_plot.SetHeight(0.8)"
        self.renderer.addToEvalStack(evalString)

        return

    def render(self):
        """
        Does LinePlot object specific (pre)rendering stuff
        """
        debugMsg("Called LinePlot.render()")

        self.renderer.addToEvalStack("# LinePlot.render()")
        self.renderer.addToEvalStack("_renderer.AddActor2D(_plot)")

        # set the title if set
        if self.title is not None:
            evalString = "_plot.SetTitle(\'%s\')" % self.title
            self.renderer.addToEvalStack(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_plot.SetXTitle(\'%s\')" % self.xlabel
            self.renderer.addToEvalStack(evalString)

        # if an ylabel is set, add it
        if self.ylabel is not None:
            evalString = "_plot.SetYTitle(\'%s\')" % self.ylabel
            self.renderer.addToEvalStack(evalString)

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

        self.renderer.addToEvalStack("# OffsetPlot.setData()")

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
            self.renderer.addToEvalStack(evalString)
        # if have two arrays to plot, the first one is the t data
        elif len(dataList) == 2:
            tData = dataList[0]
            ## generate the evalString for the x data
            evalString = "_t = array(["
            for j in range(len(tData)-1):
                evalString += "%s, " % tData[j]
            evalString += "%s])" % tData[-1]
            # give it to the renderer
            self.renderer.addToEvalStack(evalString)
            # don't need the first element of the dataList, so get rid of it
            dataList = dataList[1:]
        elif len(dataList) == 3:
            ## generate the evalString for the t data
            evalString = "_t = array(["
            for j in range(len(tData)-1):
                evalString += "%s, " % tData[j]
            evalString += "%s])" % tData[-1]
            # give it to the renderer
            self.renderer.addToEvalStack(evalString)
            ## generate the evalString for the x data
            evalString = "_x = array(["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s])" % xData[-1]
            # give it to the renderer
            self.renderer.addToEvalStack(evalString)
        else:
            # shouldn't get to here, but raise an error anyway
            raise ValueError, "Incorrect number of arguments"

        # set up the vtkDataArray object for the t data
        self.renderer.addToEvalStack(
                "_tData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)")
        self.renderer.addToEvalStack(
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
            self.renderer.addToEvalStack(evalString)

        # concatenate the data
        evalString = "_yAll = concatenate(["
        for i in range(dataLen-1):
            evalString += "_y%d," % i
        evalString += "_y%d])" % int(dataLen-1)
        self.renderer.addToEvalStack(evalString)

        # grab the min and max values
        self.renderer.addToEvalStack("_yMax = max(_yAll)")
        self.renderer.addToEvalStack("_yMin = min(_yAll)")

        # keep the data apart a bit
        if self.sep is None:
            self.renderer.addToEvalStack("_const = 0.1*(_yMax - _yMin)")
        else:
            evalString = "_const = %f" % self.sep
            self.renderer.addToEvalStack(evalString)

        # behave differently with the shift if we have xData as to not
        if len(dataList) == 3:
            # this is for when we have xData
            self.renderer.addToEvalStack("_yMaxAbs = max(abs(_yAll))")
            # calculate the minimum delta x
            x1 = xData[:-1]
            x2 = xData[1:]
            minDeltax = min(x2 - x1)
            evalString = "_scale = %f/(2.0*_yMaxAbs)" % minDeltax
            self.renderer.addToEvalStack(evalString)

            for i in range(dataLen):
                evalString = "_y%d = _scale*_y%d + _x[%d]" % (i, i, i)
                self.renderer.addToEvalStack(evalString)
        else:
            # shift the data up
            self.renderer.addToEvalStack("_shift = _yMax - _yMin + _const")

            for i in range(dataLen):
                evalString = "_y%d = _y%d + %f*_shift" % (i, i, i)
                self.renderer.addToEvalStack(evalString)

        # set up the vtkDataArray objects
        for i in range(dataLen):
            evalString = \
            "_y%dData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)\n" % i
            evalString += "_y%dData.SetNumberOfTuples(len(_y%d))" % (i, i)
            self.renderer.addToEvalStack(evalString)

        ## t data
        # put the data into the data arrays
        self.renderer.addToEvalStack("for i in range(len(_t)):")
        # need to be careful here to remember to indent the code properly
        evalString = "    _tData.SetTuple1(i,_t[i])"
        self.renderer.addToEvalStack(evalString)

        ## y data
        # put the data into the data arrays
        self.renderer.addToEvalStack("for i in range(len(_t)):")
        # need to be careful here to remember to indent the code properly
        for i in range(dataLen):
            evalString = "    _y%dData.SetTuple1(i,_y%d[i])" % (i, i)
            self.renderer.addToEvalStack(evalString)

        for i in range(dataLen):
            # create the field data object
            evalString = "_fieldData%d = vtk.vtkFieldData()" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AllocateArrays(2)" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AddArray(_tData)" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AddArray(_y%dData)" % (i, i)
            self.renderer.addToEvalStack(evalString)

        for i in range(dataLen):
            # now put the field data into a data object
            evalString = "_dataObject%d = vtk.vtkDataObject()\n" % i
            evalString += "_dataObject%d.SetFieldData(_fieldData%d)\n" % (i, i)

            # the actor should be set up, so add the data object to the actor
            evalString += "_plot.AddDataObjectInput(_dataObject%d)" % i
            self.renderer.addToEvalStack(evalString)

        # tell the actor to use the x values for the x values (rather than
        # the index)
        self.renderer.addToEvalStack("_plot.SetXValuesToValue()")

        # set which parts of the data object are to be used for which axis
        self.renderer.addToEvalStack("_plot.SetDataObjectXComponent(0,0)")
        for i in range(dataLen):
            evalString = "_plot.SetDataObjectYComponent(%d,1)" % i
            self.renderer.addToEvalStack(evalString)

        # note: am ignoring zlabels as vtk xyPlot doesn't support that
        # dimension for line plots (I'll have to do something a lot more
        # funky if I want that kind of functionality)

        return

    def render(self):
        """
        Does OffsetPlot object specific (pre)rendering stuff
        """
        debugMsg("Called OffsetPlot.render()")

        self.renderer.addToEvalStack("# OffsetPlot.render()")
        self.renderer.addToEvalStack("_renderer.AddActor2D(_plot)")

        # set the title if set
        if self.title is not None:
            evalString = "_plot.SetTitle(\'%s\')" % self.title
            self.renderer.addToEvalStack(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_plot.SetXTitle(\'%s\')" % self.xlabel
            self.renderer.addToEvalStack(evalString)

        # if an ylabel is set, add it
        if self.ylabel is not None:
            evalString = "_plot.SetYTitle(\'%s\')" % self.ylabel
            self.renderer.addToEvalStack(evalString)

        return

# vim: expandtab shiftwidth=4:

