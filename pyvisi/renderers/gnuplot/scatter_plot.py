# Copyright (C) 2004-2008 Paul Cochrane
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


"""
Class and functions associated with a pyvisi ScatterPlot objects (gnuplot)
"""

# generic imports
from pyvisi.renderers.gnuplot.common import debugMsg
import copy

# module specific imports
from pyvisi.renderers.gnuplot.plot import Plot

__revision__ = '$Revision$'

class ScatterPlot(Plot):
    """
    Scatter plot 
    
    Plots a scatter data points in 2D, for 3D scatter plots use ScatterPlot3D
    """

    def __init__(self, scene):
        """
        Initialisation of ScatterPlot class

        @param scene: the scene with which to associate the ScatterPlot
        @type scene: Scene object
        """
        debugMsg("Called ScatterPlot.__init__()")
        Plot.__init__(self, scene)

        # grab the renderer
        self.renderer = scene.renderer

        # set up some of the attributes
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None
        
        # now add the object to the scene
        scene.add(self)

    def setData(self, *dataList, **options):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple

        @param options: dictionary of extra options
        @type options: dict
        """
        debugMsg("Called setData() in ScatterPlot()")

        self.renderer.runString("# ScatterPlot.setData()")

        # do some sanity checking on the data
        for i in range(len(dataList)):
            if len(dataList[0]) != len(dataList[i]):
                raise ValueError, "Input vectors must all be the same length"

        # if have more than one array to plot the first one is the x data
        if len(dataList) > 1:
            xData = dataList[0]
            ## pass around the x data
            self.renderer.renderDict['_x'] = copy.deepcopy(xData)
            # don't need the first element of the dataList so get rid of it
            dataList = dataList[1:]
        # if only have one array input, then autogenerate the xData
        elif len(dataList) == 1:
            xData = range(1, len(dataList[0])+1)
            if len(xData) != len(dataList[0]):
                errorString = "Autogenerated xData array length not "
                errorString += "equal to input array length"
                raise ValueError, errorString

            ## pass around the x data
            self.renderer.renderDict['_x'] = copy.deepcopy(xData)

        # range over the data, printing what the expansion of the array is
        # and regenerate the data within the eval
        for i in range(len(dataList)):
            yDataVar = "_y%d" % i
            data = dataList[i]
            # check that the data here is a 1-D array
            if len(data.shape) != 1:
                raise ValueError, "Can only handle 1D arrays at present"

            self.renderer.renderDict[yDataVar] = copy.deepcopy(data)

            evalString = "_data%d = Gnuplot.Data(_x, " % i
            evalString += "_y%d" % i

            # this is the linestyle that makes this a scatter plot
            evalString += ", with='points pointtype 2'"

            # finish off the evalString
            evalString += ")"

            # and add it to the evalstack
            self.renderer.runString(evalString)

        # return the number of objects to plot
        self.renderer.numDataObjects = len(dataList)

        return

    def render(self):
        """
        Does ScatterPlot object specific rendering stuff
        """
        debugMsg("Called ScatterPlot.render()")

        self.renderer.runString("# ScatterPlot.render()")

        # if a title is set, put it here
        if self.title is not None:
            evalString = "_gnuplot.title(\'%s\')" % self.title
            self.renderer.runString(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_gnuplot.xlabel(\'%s\')" % self.xlabel
            self.renderer.runString(evalString)

        # if a ylabel is set, add it
        if self.ylabel is not None:
            evalString = "_gnuplot.ylabel(\'%s\')" % self.ylabel
            self.renderer.runString(evalString)

        # if a zlabel is set, add it
        if self.zlabel is not None:
            evalString = "_gnuplot('set zlabel \\'%s\\'')" % self.zlabel
            self.renderer.runString(evalString)

        # set up the evalString to use for plotting
        evalString = "_gnuplot.plot("
        for i in range(self.renderer.numDataObjects-1):
            evalString += "_data%d, " % i
        evalString += "_data%d)" % (self.renderer.numDataObjects-1,)
        self.renderer.runString(evalString)

        return


# vim: expandtab shiftwidth=4:
