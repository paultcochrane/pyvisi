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

    def setData(self, *dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in ArrowPlot()")

        if dataList is None:
            raise ValueError, "You must specify a data list"
        
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

    def setData(self, *dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in ContourPlot()")

        if dataList is None:
            raise ValueError, "You must specify a data list"

        return

    def render(self):
        """
        Does ContourPlot object specific (pre)rendering stuff
        """
        debugMsg("Called ContourPlot.render()")

        self.renderer.addToEvalStack("# ContourPlot.render()")

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

