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
from pyvisi.renderers.povray.common import debugMsg

# module specific imports
from pyvisi.renderers.povray.item import Item

from Numeric import *

__revision__ = '$Revision$'

class Plot(Item):
    """
    Abstract plot class
    """
    def __init__(self, scene):
        """
        Initialisation of Plot class

        @param scene: the scene with which to associate the plot
        @type scene: Scene object
        """
        debugMsg("Called Plot.__init__()")
        Item.__init__(self)

        if scene is None:
            raise ValueError, "You must specify a scene object"

    def setData(self, *dataList):
        """
        Set the data to the plot

        @param dataList: list of data objects to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in Plot()")

        if dataList is None:
            raise ValueError, "You must specify a data list"
        
        return

class ArrowPlot(Plot):
    """
    Arrow field plot
    """
    def __init__(self, scene):
        """
        Initialisation of the ArrowPlot class

        @param scene: the scene with which to associate the arrow plot
        @type scene: Scene object
        """
        debugMsg("Called ArrowPlot.__init__()")
        Plot.__init__()

        if scene is None:
            raise ValueError, "You must specify a scene object"

    def setData(self, *dataList):
        """
        Set data to the plot

        @param dataList: list/tuple of data objects to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in ArrowPlot()")

        if dataList is None:
            raise ValueError, "You must specify a data list"
        
        return

class BallPlot(Plot):
    """
    Ball plot
    """
    def __init__(self, scene):
        debugMsg("Called BallPlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer
        self.renderer.addToEvalStack("// BallPlot.__init__()")

        # the data to pass between setData() and render()
        self.x = None
        self.y = None
        self.z = None
        self.radii = None

        # the colour info to pass between setData() and render()
        self.red = None
        self.green = None
        self.blue = None

        # add the plot to the scene
        scene.add(self)

    def setData(self, points=None, radii=None, tags=None, colors=None,
            fname=None, format=None):
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
        self.renderer.addToEvalStack("// BallPlot.setData()")

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
            # we're using vtk to read in the data, so import the module
            import vtk

            if format == "vtk-xml":
                debugMsg("Using vtk-xml file as input")
                # create the reader of the file
                reader = vtk.vtkXMLUnstructuredGridReader()
                reader.SetFileName(fname)
                reader.Update()
            elif format == "vtk":
                debugMsg("Using old-style vtk file as input")
                # create the reader of the file
                reader = vtk.vtkUnstructuredGridReader()
                reader.SetFileName(fname)
                reader.Update()

            # read the output to an unstructured grid
            grid = reader.GetOutput()

            modelCentre = grid.GetCenter()
            xMin, xMax, yMin, yMin, zMin, zMax = grid.GetBounds()

            # grab the points where the data sit
            vtkPoints = grid.GetPoints()

            # note that these next few steps are only necessary in vtk 4.2,
            # 4.4 grab the data to use for the radii of the balls
            vtkRadii = grid.GetPointData().GetScalars(radii)
    
            # grab the data to use for colouring the balls
            vtkTags = grid.GetPointData().GetScalars(tags)
    
            # now work out the number of tags, and their values
            numPoints = vtkTags.GetNumberOfTuples()
            valueDict = {}
            for i in range(numPoints):
                tagValue = vtkTags.GetValue(i)
                valueDict[tagValue] = 1
    
            numTags = len(valueDict.keys())
    
            tagValues = valueDict.keys()
            tagValues.sort()
    
            # now count the number of tags, and make an evenly spaced
            # array of points between zero and one, then use these as the
            # scalars to colour by
            vtkScaledTags = vtk.vtkFloatArray()
            vtkScaledTags.SetNumberOfTuples(numPoints)
            vtkScaledTags.SetNumberOfComponents(1)
            vtkScaledTags.SetName("scaledTags")
            if numTags == 1:
                for i in range(numPoints):
                    vtkScaledTags.InsertTuple1(i, 0.0)
            else:
                for i in range(numPoints):
                    tagValue = vtkTags.GetValue(i)
                    for j in range(numTags):
                        if tagValues[j] == tagValue:
                            vtkScaledTags.InsertTuple1(i, \
                                    float(j)/float(numTags-1))

            # use vtk to generate the colour map, will have to do this
            # myself for the non-vtk loading version
            lut = vtk.vtkLookupTable()
            lut.Build()

            red = zeros(numPoints, typecode=Float)
            green = zeros(numPoints, typecode=Float)
            blue = zeros(numPoints, typecode=Float)
            for i in range(numPoints):
                red[i], green[i], blue[i] = \
                        lut.GetColor(vtkScaledTags.GetValue(i))

            # now convert the information we want (radii, colours,
            # positions) into array objects so that I can play with them as
            # per normal in python

            x = zeros(numPoints, typecode=Float)
            y = zeros(numPoints, typecode=Float)
            z = zeros(numPoints, typecode=Float)
            radii = zeros(numPoints, typecode=Float)
            scaledTags = zeros(numPoints, typecode=Float)
            tags = zeros(numPoints, typecode=Float)
            for i in range(numPoints):
                ### the points
                x[i], y[i], z[i] = vtkPoints.GetPoint(i)

                ### the radii
                radii[i] = vtkRadii.GetValue(i)

                ### the tags
                scaledTags[i] = vtkScaledTags.GetValue(i)
                tags[i] = vtkTags.GetValue(i)
    
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

            ### get the x, y, z data from the points
            x = zeros(numPoints, typecode=Float)
            y = zeros(numPoints, typecode=Float)
            z = zeros(numPoints, typecode=Float)

            for i in range(numPoints):
                x[i], y[i], z[i] = points[i]

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

            # now scale the tags
            scaledTags = zeros(numPoints, typecode=Float)
            if numTags == 1:
                pass
            else:
                for i in range(numPoints):
                    for j in range(numTags):
                        if tagValues[j] == tags[i]:
                            scaledTags[i] = float(j)/float(numTags-1)
        else:
            # barf
            raise ValueError, \
                    "Cannot construct BallPlot with the given input.  Exiting."

        # share the data around
        self.x = x
        self.y = y
        self.z = z
        self.radii = radii

        # share the colours around
        self.red = red
        self.green = green
        self.blue = blue

        return

    def render(self):
        """
        Does BallPlot specific rendering tasks
        """
        debugMsg("Called render() in BallPlot")
        self.renderer.addToEvalStack("// BallPlot.render()")

        # grab the data
        x = self.x
        y = self.y
        z = self.z
        radii = self.radii

        # grab the colours
        red = self.red
        green = self.green
        blue = self.blue

        evalString = ""
        for i in range(len(x)):
            evalString += "sphere {\n"
            evalString += "  <%f, %f, %f> %f\n" % (x[i], y[i], z[i], radii[i])
            evalString += "  pigment {\n"
            evalString += "    rgb <%f, %f, %f>\n" % (red[i], green[i], blue[i])
            evalString += "  }\n"
            evalString += "}\n"

        self.renderer.addToEvalStack(evalString)

        # set the title if set
        if self.title is not None:
            # not implemented yet
            pass

        return
 

class ContourPlot(Plot):
    """
    Contour plot
    """
    def __init__(self, scene):
        """
        Initialisation of the ContourPlot class
        
        @param scene: the scene with which to associate the contour plot
        @type scene: Scene object
        """
        debugMsg("Called ContourPlot.__init__()")
        Plot.__init__()

        if scene is None:
            raise ValueError, "You must specify a scene object"

    def setData(self, *dataList):
        """
        Set data to the plot

        @param dataList: list/tuple of data to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in ContourPlot()")

        if dataList is None:
            raise ValueError, "You must specify a data list"
        
        return

class LinePlot(Plot):
    """
    Line plot
    """
    def __init__(self, scene):
        """
        Initialisation of the ContourPlot class
        
        @param scene: the scene with which to associate the line plot
        @type scene: Scene object
        """
        debugMsg("Called LinePlot.__init__()")
        Plot.__init__()

        if scene is None:
            raise ValueError, "You must specify a scene object"

    def setData(self, *dataList):
        """
        Set data to the plot

        @param dataList: list/tuple of data to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in LinePlot()")

        if dataList is None:
            raise ValueError, "You must specify a data list"
        
        return

# vim: expandtab shiftwidth=4:

