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

## @file plot.py

"""
Class and functions associated with a pyvisi Plot objects
"""

# generic imports
from common import _debug, rendererName

# module specific imports
from item import Item

class Plot(Item):
    """
    Abstract plot class
    """
    def __init__(self,scene):
        """
        Initialisation of the abstract Plot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called Plot.__init__()" % rendererName
        pass

    def setData(self,*dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called setData() in Plot()" % rendererName
        return True

    def setTitle(self,title):
        """
        Set the plot title

        @param title: the string holding the title to the plot
        """
        if _debug: print "\t%s: Called setTitle() in Plot()" % rendererName

        self.title = title

        return

    def setXLabel(self,label):
        """
        Set the label of the x-axis

        @param label: the string holding the label of the x-axis
        """
        if _debug: print "\t%s: Called setXLabel() in Plot()" % rendererName

        self.xlabel = label

        return

    def setYLabel(self,label):
        """
        Set the label of the y-axis

        @param label: the string holding the label of the y-axis
        """
        if _debug: print "\t%s: Called setYLabel() in Plot()" % rendererName

        self.ylabel = label

        return

    def setZLabel(self,label):
        """
        Set the label of the z-axis

        @param label: the string holding the label of the z-axis
        """
        if _debug: print "\t%s: Called setZLabel() in Plot()" % rendererName

        self.zlabel = label

        return

    def setLabel(self,axis,label):
        """
        Set the label of a given axis

        @param axis: string (Axis object maybe??) of the axis (e.g. x, y, z)
        @param label: string of the label to set for the axis
        """
        if _debug: print "\t%s: Called setLabel() in Plot()" % rendererName

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
        if _debug: print "\t%s: Called Plot.render()" % rendererName

        return

class ArrowPlot(Plot):
    """
    Arrow field plot
    """
    def __init__(self,scene):
        """
        Initialisation of the ArrowPlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called ArrowPlot.__init__()" % rendererName
        return

    def setData(self,*dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called setData() in ArrowPlot()" % rendererName
        return True

class ContourPlot(Plot):
    """
    Contour plot
    """
    def __init__(self,scene):
        """
        Initialisation of the ContourPlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called ContourPlot.__init__()" % rendererName
        return

    def setData(self,*dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called setData() in ContourPlot()"%rendererName
        return True

class LinePlot(Plot):
    """
    Line plot
    """
    def __init__(self,scene):
        """
        Initialisation of the LinePlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called LinePlot.__init__()" % rendererName

        self.renderer = scene.renderer
        self.renderer.addToEvalStack("# LinePlot.__init__()")
        self.renderer.addToEvalStack("_plot = vtk.vtkXYPlotActor()")

        return True

    def setData(self,*dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called setData() in LinePlot()" % rendererName

        self.renderer.addToEvalStack("# LinePlot.setData()")

        # do some sanity checking on the data
        for i in range(len(dataList)):
            if len(dataList[0]) != len(dataList[i]):
                raise DataError, "Input vectors must all be the same length"

        # if have more than one array to plot, the first one is the x data
        if len(dataList) > 1:
            xData = dataList[0]
            ## generate the evalString for the x data
            evalString = "_x = ["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s]" % xData[-1]
            # give it to the renderer
            self.renderer.addToEvalStack(evalString)
            # don't need the first element of the dataList, so get rid of it
            dataList = dataList[1:]
            # if only have one array input, then autogenerate xData
        elif len(dataList) == 1:
            xData = arange(1,len(dataList[0]))
            ## generate the evalString for the x data
            evalString = "_x = ["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s]" % xData[-1]
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
            evalString = "_y%d = [" % i
            data = dataList[i]
            # check that the data here is a 1-D array
            if len(data.shape) != 1:
                raise ValueError, "Can only handle 1D arrays at present"

            for j in range(len(data)-1):
                evalString += "%s, " % data[j]
            evalString += "%s]" % data[-1]
            self.renderer.addToEvalStack(evalString)

        # set up the vtkDataArray objects
        for i in range(len(dataList)):
            evalString = \
            "_y%dData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)\n" % i
            evalString += "_y%dData.SetNumberOfTuples(len(_y%d))" % (i,i)
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
            evalString = "    _y%dData.SetTuple1(i,_y%d[i])" % (i,i)
            self.renderer.addToEvalStack(evalString)

        for i in range(len(dataList)):
            # create the field data object
            evalString = "_fieldData%d = vtk.vtkFieldData()" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AllocateArrays(2)" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AddArray(_xData)" % i
            self.renderer.addToEvalStack(evalString)
            evalString = "_fieldData%d.AddArray(_y%dData)" % (i,i)
            self.renderer.addToEvalStack(evalString)

        for i in range(len(dataList)):
            # now put the field data into a data object
            evalString = "_dataObject%d = vtk.vtkDataObject()\n" % i
            evalString += "_dataObject%d.SetFieldData(_fieldData%d)\n" % (i,i)

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

        return True

    def render(self):
        """
        Does LinePlot object specific (pre)rendering stuff
        """
        if _debug: print "\t%s: Called LinePlot.render()" % rendererName

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

# vim: expandtab shiftwidth=4:

