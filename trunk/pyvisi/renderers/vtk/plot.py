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
        pass

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
        pass

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

        # check the length of the data list
        if (len(dataList)) != 2:
            raise ValueError, "Must have two 1D arrays as input (at present)"

        # now to add my dodgy hack until I have a decent way of sharing data
        # objects around properly
        for i in range(len(dataList)):
            evalString = "_x%d = [" % i
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
            "_x%dData = vtk.vtkDataArray.CreateDataArray(vtk.VTK_FLOAT)\n" % i
            evalString += "_x%dData.SetNumberOfTuples(len(_x%d))" % (i,i)
            self.renderer.addToEvalStack(evalString)

        # put the data into the data arrays
        self.renderer.addToEvalStack("for i in range(len(_x0)):")
        # need to be careful here to remember to indent the code properly
        for i in range(len(dataList)):
            evalString = "    _x%dData.SetTuple1(i,_x%d[i])" % (i,i)
            self.renderer.addToEvalStack(evalString)

        # create the field data object
        self.renderer.addToEvalStack("_fieldData = vtk.vtkFieldData()")
        self.renderer.addToEvalStack("_fieldData.AllocateArrays(2)")
        for i in range(len(dataList)):
            evalString = "_fieldData.AddArray(_x%dData)" % i
            self.renderer.addToEvalStack(evalString)

        # now put the field data into a data object
        self.renderer.addToEvalStack("_dataObject = vtk.vtkDataObject()")
        self.renderer.addToEvalStack("_dataObject.SetFieldData(_fieldData)")

        # the actor should be set up, so add the data object to the actor
        self.renderer.addToEvalStack("_plot.AddDataObjectInput(_dataObject)")

        # tell the actor to use the x values for the x values (rather than
        # the index)
        self.renderer.addToEvalStack("_plot.SetXValuesToValue()")

        # set which parts of the data object are to be used for which axis
        self.renderer.addToEvalStack("_plot.SetDataObjectXComponent(0,0)")
        self.renderer.addToEvalStack("_plot.SetDataObjectYComponent(0,1)")


        # don't really know if this should go in here or somewhere else...
        # I've got this kind of code in this method in the gnuplot library,
        # and maybe it's not the best place to have it.

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

        return

# vim: expandtab shiftwidth=4:

